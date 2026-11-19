package quietcraft.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;

final class GameScreens {
    static Screen current(Minecraft game) {
        return game.gui.screen();
    }

    static void show(Minecraft game, Screen screen) {
        game.gui.setScreen(screen);
    }
}
