# Quiet Craft

Quiet Craft adds opt-in ASMR ambience to Minecraft Java Edition. Each player chooses rain, campfire crackles, or cave drips. The server plays quiet vanilla sounds with randomized pauses and remembers each player's choice across reconnects.

| Minecraft | Loaders | Java |
| --- | --- | --- |
| 1.21.4 | Fabric, Forge | 21 |
| 1.21.11 | Fabric, Forge | 21 |
| 26.1 | Fabric, Forge | 25 |
| 26.2 | Fabric, Forge | 25 |

Build all eight JARs with `python build.py`. Requires Python 3.8 or newer. Install only the JAR that matches your game version and loader in the server's `mods/` folder, then restart. On Fabric, install [Fabric API](https://modrinth.com/mod/fabric-api) for the same Minecraft version. The server script installs it automatically. The mod also works in a local single-player world with the matching loader.

## Start a dedicated server

Install Python and the Java version from the table. Read the [Minecraft EULA](https://aka.ms/MinecraftEULA) before using the acceptance flag.

```sh
python server.py 26.2 fabric --accept-eula
```

Replace the arguments with your game version and `fabric` or `forge`. Use `--java /path/to/java` if the correct Java is outside your PATH. Each combination stores its own world and settings under `servers/<loader>-<version>/`. Stop one server before starting another on the default port. Join with Minecraft on the same version at `localhost:25565`. To let other players join, run the same command on your server host and give them its address. The mod uses vanilla sounds and commands, so a matching server-compatible client does not need a copy of Quiet Craft.

## Choose your sounds

| Command | Effect |
| --- | --- |
| `/trigger asmr set 5` | Show the choices |
| `/trigger asmr set 1` | Rain |
| `/trigger asmr set 2` | Campfire |
| `/trigger asmr set 3` | Cave drips |
| `/trigger asmr set 4` | Off |

The effects use Minecraft's Ambient/Environment volume slider. They are off by default, and players can use the commands without operator permissions.
