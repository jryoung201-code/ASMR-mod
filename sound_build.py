"""Turn a track from the Quiet Craft sound API into Minecraft assets."""
import json
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from pathlib import Path
from urllib.request import urlopen

MAX_AUDIO_BYTES = 64 * 1024 * 1024


def minecraft_audio(api_url, sound_id):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", sound_id):
        raise ValueError("Sound ID must be a lowercase catalog identifier.")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("Install FFmpeg to build with a custom sound.")
    url = f"{api_url.rstrip('/')}/api/v1/sounds/{sound_id}/audio"
    with TemporaryDirectory() as directory:
        source = Path(directory) / "source"
        output = Path(directory) / "ambience.ogg"
        with urlopen(url, timeout=60) as response:
            audio = response.read(MAX_AUDIO_BYTES + 1)
        if not audio or len(audio) > MAX_AUDIO_BYTES:
            raise ValueError("Audio must be non-empty and at most 64 MiB.")
        source.write_bytes(audio)
        subprocess.run([
            ffmpeg, "-nostdin", "-hide_banner", "-loglevel", "error", "-i",
            str(source), "-vn", "-c:a", "libvorbis", "-q:a", "4", str(output),
        ], check=True)
        return output.read_bytes()


def write_audio(jar, audio):
    jar.writestr("assets/quiet_craft/sounds/custom.ogg", audio)
    jar.writestr("assets/quiet_craft/sounds.json", json.dumps({
        "custom": {"sounds": [{
            "name": "quiet_craft:custom", "stream": True, "attenuation_distance": 256,
        }]},
    }))
