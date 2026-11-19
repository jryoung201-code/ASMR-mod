"""Build the eight Quiet Craft mod JARs with Python 3.8+."""
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parent
VERSION = "0.1.0"
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


def build(game, loader):
    java, pack_format, forge_version = TARGETS[game]
    output = ROOT / "dist" / f"quiet-craft-{VERSION}-{loader}-{game}.jar"
    output.parent.mkdir(exist_ok=True)
    pack = {"description": "Quiet Craft ambience"}
    if game == "1.21.4":
        pack["pack_format"] = pack_format[0]
    else:
        pack.update(min_format=pack_format, max_format=pack_format)

    with ZipFile(output, "w", ZIP_DEFLATED) as jar:
        for source in sorted((ROOT / "pack").rglob("*")):
            if source.is_file():
                jar.write(source, source.relative_to(ROOT / "pack").as_posix())
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
    for game_version in TARGETS:
        for mod_loader in ("fabric", "forge"):
            print(build(game_version, mod_loader).relative_to(ROOT))
