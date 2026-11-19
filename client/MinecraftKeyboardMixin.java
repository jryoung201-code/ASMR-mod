package quietcraft.client;

import net.minecraft.client.KeyboardHandler;
import net.minecraft.client.Minecraft;
import net.minecraft.client.input.KeyEvent;
import org.lwjgl.glfw.GLFW;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(KeyboardHandler.class)
public abstract class MinecraftKeyboardMixin {
    @Inject(method = "keyPress", at = @At("HEAD"), cancellable = true, remap = false)
    private void quietCraftOpenMenu(long window, int action, KeyEvent event, CallbackInfo callback) {
        Minecraft game = Minecraft.getInstance();
        if (action == GLFW.GLFW_PRESS && event.key() == GLFW.GLFW_KEY_GRAVE_ACCENT
                && GLFW.glfwGetKey(window, GLFW.GLFW_KEY_LEFT_SHIFT) == GLFW.GLFW_PRESS
                && game.player != null && GameScreens.current(game) == null) {
            GameScreens.show(game, new SoundMenu());
            callback.cancel();
        }
    }
}
