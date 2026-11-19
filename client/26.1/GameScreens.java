package quietcraft.client;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;

final class GameScreens {
    static Screen current(Minecraft game) {
        return game.screen;
    }

    static void show(Minecraft game, Screen screen) {
        game.setScreen(screen);
    }
}
