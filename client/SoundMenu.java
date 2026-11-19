package quietcraft.client;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

public final class SoundMenu extends Screen {
    private int top;

    public SoundMenu() {
        super(Component.literal("Quiet Craft"));
    }

    @Override
    protected void init() {
        top = Math.max(24, (height - 136) / 2);
        addSound("Soft Rain", 1, 0);
        addSound("Campfire", 2, 1);
        addSound("Cave Drips", 3, 2);
        addSound("Custom Track", 6, 3);
        addSound("Stop Sounds", 4, 4);
        addRenderableWidget(Button.builder(Component.literal("Back"), button -> onClose())
                .bounds(width / 2 - 89, top + 112, 178, 20).build());
    }

    private void addSound(String label, int selection, int row) {
        addRenderableWidget(Button.builder(Component.literal(label), button -> {
            var connection = minecraft.getConnection();
            if (connection != null) {
                connection.sendCommand("trigger asmr set " + selection);
            }
            onClose();
        }).bounds(width / 2 - 89, top + row * 22, 178, 20).build());
    }

    @Override
    public void extractRenderState(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick) {
        super.extractRenderState(graphics, mouseX, mouseY, partialTick);
        graphics.centeredText(font, title, width / 2, top - 17, 0xFFF3EBDD);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
