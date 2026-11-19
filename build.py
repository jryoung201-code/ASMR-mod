"""Build the eight Quiet Craft mod JARs with Python 3.8+."""
import argparse
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from sound_build import minecraft_audio, write_audio

ROOT = Path(__file__).resolve().parent
VERSION = "0.2.0"
TARGETS = {
    "1.21.4": (21, (61, 0), "54.1.22"),
    "1.21.11": (21, (94, 1), "61.2.4"),
    "26.1": (25, (101, 1), "62.0.4"),
    "26.2": (25, (107, 1), "65.1.5"),
}
FABRIC_API = {
    "1.21.4": "0.119.4+1.21.4",
    "1.21.11": "0.141.6+1.21.11",
    "26.1": "0.145.1+26.1",
    "26.2": "0.161.0+26.2",
}
RESOURCE_FORMATS = {
    "1.21.4": (46, 0),
    "1.21.11": (75, 0),
    "26.1": (84, 0),
    "26.2": (88, 0),
}


def build(game, loader, audio=None):
    java, pack_format, forge_version = TARGETS[game]
    variant = "" if audio is None else "-custom"
    output = ROOT / "dist" / f"quiet-craft-{VERSION}-{loader}-{game}{variant}.jar"
    output.parent.mkdir(exist_ok=True)
    pack = {"description": "Quiet Craft ambience"}
    resource_format = RESOURCE_FORMATS[game] if audio is not None else pack_format
    if game == "1.21.4":
        pack["pack_format"] = pack_format[0]
        if audio is not None:
            pack["supported_formats"] = [resource_format[0], pack_format[0]]
    else:
        pack.update(min_format=resource_format, max_format=pack_format)

    with ZipFile(output, "w", ZIP_DEFLATED) as jar:
        for source in sorted((ROOT / "pack").rglob("*")):
            if source.is_file():
                archive_path = source.relative_to(ROOT / "pack").as_posix()
                if audio is not None and source.name == "custom.mcfunction":
                    jar.writestr(archive_path, (
                        "scoreboard players set @s qc_mode 4\n"
                        "stopsound @s ambient quiet_craft:custom\n"
                        "playsound quiet_craft:custom ambient @s ~ ~1.5 ~ 0.35 1 0.25\n"
                    ))
                else:
                    jar.write(source, archive_path)
        if audio is not None:
            write_audio(jar, audio)
        jar.writestr("pack.mcmeta", json.dumps({"pack": pack}))
        if loader == "fabric":
            jar.writestr("fabric.mod.json", json.dumps({
                "schemaVersion": 1,
                "id": "quiet_craft",
                "name": "Quiet Craft",
                "version": VERSION,
                "description": "Opt-in rain, campfire and cave ambience.",
                "environment": "*",
                "depends": {
                    "minecraft": game,
                    "fabricloader": "*",
                    "fabric-api": "*",
                    "java": f">={java}",
                },
            }))
        else:
            major = forge_version.split(".")[0]
            jar.writestr("META-INF/mods.toml", f'''modLoader="lowcodefml"
loaderVersion="[{major},{int(major) + 1})"
license="All Rights Reserved"

[[mods]]
modId="quiet_craft"
version="{VERSION}"
displayName="Quiet Craft"
displayTest="IGNORE_SERVER_VERSION"
description="Opt-in rain, campfire and cave ambience."

[[dependencies.quiet_craft]]
modId="minecraft"
mandatory=true
versionRange="[{game}]"
ordering="NONE"
side="BOTH"
''')
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sound-api", help="Base URL for a running Quiet Craft sound API")
    parser.add_argument("--sound-id", default="plastic-container-tapping")
    args = parser.parse_args()
    audio = minecraft_audio(args.sound_api, args.sound_id) if args.sound_api else None
    for game_version in TARGETS:
        for mod_loader in ("fabric", "forge"):
            print(build(game_version, mod_loader, audio).relative_to(ROOT))
