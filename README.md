# Quiet Craft

Quiet Craft adds opt-in ASMR ambience to Minecraft Java Edition. Each player chooses rain, campfire crackles, or cave drips. The server plays quiet vanilla sounds with randomized pauses and remembers each player's choice across reconnects.

| Minecraft | Loaders | Java |
| --- | --- | --- |
| 1.21.4 | Fabric, Forge | 21 |
| 1.21.11 | Fabric, Forge | 21 |
| 26.1 | Fabric, Forge | 25 |
| 26.2 | Fabric, Forge | 25 |

Build all eight JARs with `python build.py`. Requires Python 3.8 or newer. Install only the JAR that matches your game version and loader in the server's `mods/` folder, then restart. On Fabric, install [Fabric API](https://modrinth.com/mod/fabric-api) for the same Minecraft version. The server script installs it automatically. The mod also works in a local single-player world with the matching loader.

## Open the sound menu

In a world or on a compatible server, hold **Left Shift** and press the backtick/tilde key **`~`** directly below Escape on a US keyboard. The native menu is included in the **26.1** and **26.2** Fabric and Forge JARs whose filenames contain `-menu`. Click a sound to play it or **Stop Sounds** to turn it off. Press Escape or click **Back** to close the menu.

On **1.21.4** and **1.21.11**, run `/trigger asmr set 5` and open chat to click a sound. The chat menu also works on 26.x and on servers without the client menu installed.

To build the native menu from source, add `--client-menu` and put JDK 25's `javac` on your PATH. The build downloads and verifies the required Minecraft client artifacts.

## Host custom ASMR sounds

The [sound API repository](https://github.com/jryoung201-code/ASMR-mod-API-server) contains the standalone Render service and Google Sheets setup.

To bundle a track you can use, start the sound API and install FFmpeg. From the mod repository, run:

```sh
python build.py --client-menu --sound-api http://127.0.0.1:8080 --sound-id plastic-container-tapping
```

Use the Render HTTPS URL in place of localhost once the hosted catalog can serve the track. The build fetches the enabled sound, converts it to Ogg Vorbis, and puts it into all eight `-custom.jar` builds. To play the track, install the matching custom JAR and run `/trigger asmr set 6`. Run `/trigger asmr set 4` to stop it. On multiplayer, install the custom JAR on the server and participating clients. The game plays the embedded audio without contacting the API during gameplay.

## Optional Minecraft dedicated server

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
| `/trigger asmr set 6` | Play the bundled custom track once |

The effects use Minecraft's Ambient/Environment volume slider. They are off by default, and players can use the commands without operator permissions.
