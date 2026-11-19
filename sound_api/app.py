"""Serve ASMR audio files and a Google Sheets-backed catalog."""
import os
from pathlib import Path
import re
from threading import Lock
from time import monotonic
from urllib.parse import quote

from flask import Flask, abort, jsonify, send_file, url_for
from google.auth import default
from google.auth.exceptions import GoogleAuthError
from google.auth.transport.requests import AuthorizedSession
from requests import RequestException

SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"
COLUMNS = ["id", "title", "filename", "category", "enabled"]
SOUND_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,119}")
MIME_TYPES = {"ogg": "audio/ogg", "wav": "audio/wav", "mp3": "audio/mpeg"}
CACHE_SECONDS = 30


def parse_catalog(rows):
    if not rows or rows[0] != COLUMNS:
        raise ValueError("Sounds!A1:E1 must contain " + ", ".join(COLUMNS))

    sounds = {}
    for number, row in enumerate(rows[1:], 2):
        if not any(value != "" for value in row):
            continue
        fields = [str(value).strip() for value in (row + [""] * len(COLUMNS))[:len(COLUMNS)]]
        sound_id, title, filename, category, enabled = fields
        if enabled.lower() in ("", "false"):
            continue
        extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if (
            enabled.lower() != "true" or not SOUND_ID.fullmatch(sound_id)
            or not title or not category or not FILENAME.fullmatch(filename)
            or extension not in MIME_TYPES or sound_id in sounds
        ):
            raise ValueError(f"Invalid or duplicate enabled catalog row {number}")
        sounds[sound_id] = {
            "id": sound_id, "title": title, "filename": filename,
            "category": category, "content_type": MIME_TYPES[extension],
        }
    return sounds


def load_catalog(spreadsheet_id):
    credentials, _ = default(scopes=[SCOPE])
    sheet_range = quote("Sounds!A1:E", safe="")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{quote(spreadsheet_id, safe='')}/values/{sheet_range}"
    with AuthorizedSession(credentials) as session:
        response = session.get(url, params={"valueRenderOption": "UNFORMATTED_VALUE"}, timeout=10)
        response.raise_for_status()
        return parse_catalog(response.json().get("values", []))


def create_app(read_catalog=load_catalog):
    app = Flask(__name__)
    spreadsheet_id = os.environ.get("ASMR_SPREADSHEET_ID", "").strip()
    audio_root = Path(os.environ.get("ASMR_AUDIO_DIR", Path(__file__).parent / "audio")).resolve()
    lock = Lock()
    expires_at = 0
    cached = {}

    def catalog():
        nonlocal cached, expires_at
        with lock:
            if monotonic() >= expires_at:
                if not spreadsheet_id:
                    abort(503, description="The sound catalog is not configured.")
                try:
                    cached = read_catalog(spreadsheet_id)
                except (GoogleAuthError, RequestException, ValueError) as error:
                    app.logger.warning("Sound catalog refresh failed (%s)", type(error).__name__)
                    abort(503, description="The sound catalog is temporarily unavailable.")
                expires_at = monotonic() + CACHE_SECONDS
            return cached

    def audio_file(sound):
        path = (audio_root / sound["filename"]).resolve()
        if path.parent != audio_root or not path.is_file():
            return None
        return path

    @app.errorhandler(404)
    @app.errorhandler(503)
    def json_error(error):
        return jsonify(error=error.description), error.code

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/api/v1/sounds")
    def list_sounds():
        sounds = []
        for sound in catalog().values():
            if audio_file(sound):
                sounds.append({
                    "id": sound["id"],
                    "title": sound["title"],
                    "category": sound["category"],
                    "content_type": sound["content_type"],
                    "audio_url": url_for("get_sound", sound_id=sound["id"]),
                })
        return jsonify(sounds=sounds)

    @app.get("/api/v1/sounds/<sound_id>/audio")
    def get_sound(sound_id):
        if not SOUND_ID.fullmatch(sound_id):
            abort(404)
        sound = catalog().get(sound_id)
        path = audio_file(sound) if sound else None
        if path is None:
            abort(404)
        return send_file(path, mimetype=sound["content_type"], conditional=True)

    return app
