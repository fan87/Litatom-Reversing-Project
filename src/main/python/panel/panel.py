import imgui
import OpenGL.GL as gl
import sys
import glfw
from imgui.integrations.glfw import GlfwRenderer
import threading
import panel.renderer

close = False
def run(addon):
    print("Run init")
    def glfw_init():
        width, height = 500, 600
        window_name = "minimal ImGui/GLFW3 example"
        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        window = glfw.create_window(int(width), int(height), window_name, None, None)
        glfw.make_context_current(window)
        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)
        return window

    imgui.create_context()
    io = imgui.get_io()
    new_font = io.fonts.add_font_from_file_ttf(
        "NotoSansTC-Light.otf", 20, glyph_ranges=io.fonts.get_glyph_ranges_chinese_full()
    )
    window = glfw_init()
    impl = GlfwRenderer(window)
    while not glfw.window_should_close(window) or close:
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()
        with imgui.font(new_font):
            panel.renderer.render(addon)

        imgui.end_frame()
        gl.glClearColor(1.0, 1.0, 1.0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)
    impl.shutdown()
    glfw.terminate()


def start(addon):
    threading.Thread(target=run, args=[addon]).start()
