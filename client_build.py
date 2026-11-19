"""Compile the client menu against official unobfuscated Minecraft clients."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
MIXIN = (
    "https://maven.fabricmc.net/net/fabricmc/sponge-mixin/0.17.5+mixin.0.8.7/"
    "sponge-mixin-0.17.5+mixin.0.8.7.jar"
)
MENU_VERSIONS = ("26.1", "26.2")
LIBRARIES = {"org.lwjgl:lwjgl-glfw", "com.mojang:brigadier", "com.mojang:datafixerupper"}


def fetch_json(url):
    with urlopen(url, timeout=60) as response:
        return json.load(response)


def download(path, url, expected_sha1):
    if path.is_file() and hashlib.sha1(path.read_bytes()).hexdigest() == expected_sha1:
        return path
    with urlopen(url, timeout=90) as response:
        content = response.read()
    if hashlib.sha1(content).hexdigest() != expected_sha1:
        raise ValueError(f"Checksum mismatch for {path.name}")
    temporary = path.with_suffix(".download")
    temporary.write_bytes(content)
    temporary.replace(path)
    return path


def compile_menu(version, cache):
    sdk = cache / version
    sdk.mkdir(parents=True, exist_ok=True)
    spec = next(item for item in fetch_json(MANIFEST)["versions"] if item["id"] == version)
    metadata = fetch_json(spec["url"])
    client = metadata["downloads"]["client"]
    libraries = [download(sdk / "client.jar", client["url"], client["sha1"])]
    for library in metadata["libraries"]:
        if library["name"].rsplit(":", 1)[0] in LIBRARIES:
            artifact = library["downloads"]["artifact"]
            libraries.append(download(sdk / Path(artifact["path"]).name, artifact["url"], artifact["sha1"]))
    with urlopen(MIXIN + ".sha1", timeout=60) as response:
        mixin_sha1 = response.read().decode("ascii").strip().split()[0]
    libraries.append(download(cache / "mixin.jar", MIXIN, mixin_sha1))

    sources = ROOT / "client"
    with TemporaryDirectory() as temporary:
        output = Path(temporary)
        subprocess.run([
            "javac", "--release", "21", "-proc:none", "-classpath",
            os.pathsep.join(map(str, libraries)), "-d", str(output),
            *map(str, sorted(sources.glob("*.java"))), str(sources / version / "GameScreens.java"),
        ], check=True)
        files = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob("*.class")}
    files["quiet-craft.mixins.json"] = (sources / "quiet-craft.mixins.json").read_bytes()
    return files
