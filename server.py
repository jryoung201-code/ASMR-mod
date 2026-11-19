"""Install and run a local dedicated Minecraft server for Quiet Craft."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
from urllib.request import Request, urlopen

from build import FABRIC_API, ROOT, TARGETS, build

FABRIC_META = "https://meta.fabricmc.net/v2/versions"
FABRIC_MAVEN = "https://maven.fabricmc.net/net/fabricmc/fabric-api/fabric-api"
FORGE_MAVEN = "https://maven.minecraftforge.net/net/minecraftforge/forge"


def download(url, target):
    temporary = target.with_suffix(".download")
    request = Request(url, headers={"User-Agent": "QuietCraft-Server/0.1"})
    with urlopen(request, timeout=90) as response, temporary.open("wb") as output:
        shutil.copyfileobj(response, output)
    temporary.replace(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("game", choices=TARGETS)
    parser.add_argument("loader", choices=("fabric", "forge"))
    parser.add_argument("--accept-eula", action="store_true",
                        help="Accept the Minecraft EULA at https://aka.ms/MinecraftEULA")
    parser.add_argument("--install-only", action="store_true")
    parser.add_argument("--java", default="java", help="Java executable path")
    args = parser.parse_args()

    java = shutil.which(args.java)
    if not java:
        parser.error("Java executable not found")
    minimum_java, _, forge = TARGETS[args.game]
    print(f"Use Java {minimum_java} for Minecraft {args.game}.", flush=True)
    server = ROOT / "servers" / f"{args.loader}-{args.game}"
    server.mkdir(parents=True, exist_ok=True)

    if args.loader == "fabric":
        launcher = server / "fabric-server.jar"
        if not launcher.exists():
            with urlopen(f"{FABRIC_META}/loader/{args.game}", timeout=90) as response:
                loaders = json.load(response)
            loader = next(entry["loader"]["version"] for entry in loaders if entry["loader"]["stable"])
            with urlopen(f"{FABRIC_META}/installer", timeout=90) as response:
                installers = json.load(response)
            installer = next(entry["version"] for entry in installers if entry["stable"])
            download(f"{FABRIC_META}/loader/{args.game}/{loader}/{installer}/server/jar", launcher)
        command = [java, "-Xms1G", "-Xmx2G", "-jar", launcher.name]
    else:
        version = f"{args.game}-{forge}"
        library = Path("libraries/net/minecraftforge/forge") / version
        platform = "win" if os.name == "nt" else "unix"
        launch_args = library / f"{platform}_args.txt"
        if not (server / launch_args).exists():
            installer = server / f"forge-{version}-installer.jar"
            if not installer.exists():
                download(f"{FORGE_MAVEN}/{version}/{installer.name}", installer)
            subprocess.run([java, "-jar", installer.name, "--installServer"], cwd=server, check=True)
        if not (server / launch_args).is_file():
            raise SystemExit(f"Forge did not generate {launch_args}. Check the installer log.")
        command = [java, "-Xms1G", "-Xmx2G", f"@{launch_args.as_posix()}"]

    jar = build(args.game, args.loader)
    mods = server / "mods"
    mods.mkdir(exist_ok=True)
    if args.loader == "fabric":
        api_version = FABRIC_API[args.game]
        api = mods / f"fabric-api-{api_version}.jar"
        if not api.exists():
            download(f"{FABRIC_MAVEN}/{api_version}/{api.name}", api)
    shutil.copy2(jar, mods / jar.name)

    eula = server / "eula.txt"
    if args.accept_eula:
        eula.write_text("eula=true\n", encoding="ascii")
    print(f"Installed Quiet Craft in {server}", flush=True)
    if args.install_only:
        return
    if not eula.exists() or "eula=true" not in eula.read_text().splitlines():
        raise SystemExit("Read https://aka.ms/MinecraftEULA and rerun with --accept-eula if you agree.")
    subprocess.run([*command, "nogui"], cwd=server, check=True)


if __name__ == "__main__":
    main()
