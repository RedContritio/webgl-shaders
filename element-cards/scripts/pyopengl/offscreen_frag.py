from OpenGL.GL import *
from PIL import Image, ImageOps
import OpenGL.GL.shaders
import glfw
import numpy as np
import sys
import io
from os import path
 
VERTEX_SHADER = """
#version 330

in vec3 v_position;

void main() {
    gl_Position = vec4(v_position, 1.0);
}
"""

DEFAULT_FRAGMENT_SHADER = """
#version 330

void main() {

    gl_FragColor  = vec4(.0f, 1.0f, 0.,1 1.0f);
    
}

"""

def getShader(vshader, fshader):
    return OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vshader, GL_VERTEX_SHADER),
                                            OpenGL.GL.shaders.compileShader(fshader, GL_FRAGMENT_SHADER))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('{} fragFile [texFile]'.format(sys.argv[0]))
        exit()
        
    fragFile = sys.argv[1]
    use_tex = len(sys.argv) > 2
    if use_tex:
        texFile = sys.argv[2]

    WINDOW_WIDTH = 896
    WINDOW_HEIGHT = 1496

    if use_tex:
        textureImg = ImageOps.flip(Image.open(texFile))
        textureBytes = textureImg.tobytes()
        textureWidth, textureHeight = textureImg.size
        WINDOW_WIDTH, WINDOW_HEIGHT = 4 * textureWidth, 4 * textureHeight

    with open(fragFile, 'r') as f:
        FRAGMENT_SHADER = '\n'.join(f.readlines())
    
    if not glfw.init():
        exit()
    
    # 隐藏窗口
    glfw.window_hint(glfw.VISIBLE, False)
    # 不限制窗口高度
    glfw.window_hint(glfw.DECORATED, False)

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Only Fragment Shader", None, None)
 
    if not window:
        glfw.terminate()
        exit()
 
    glfw.make_context_current(window)
 
    vertices = [-1.0, -1.0,
                -1.0, 1.0,
                1.0, 1.0,
                1.0, -1.0]
 
    # convert to 32bit float
    vertices = np.array(vertices, dtype=np.float32)
 
    # Compile The Program and shaders
    shader = getShader(VERTEX_SHADER, FRAGMENT_SHADER)
 
    #Create EBO
    v_vertices = glGetAttribLocation(shader, 'v_position')
    glVertexAttribPointer(v_vertices, 2, GL_FLOAT, GL_FALSE, 0, vertices)
    glEnableVertexAttribArray(v_vertices)

    if use_tex:
        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, textureWidth, textureHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureBytes)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    

    # declare uniforms
    u_resolution = glGetUniformLocation(shader, "u_resolution")
    u_mouse = glGetUniformLocation(shader, "u_mouse")
    u_time = glGetUniformLocation(shader, "u_time")
    if use_tex:
        u_texTemplate = glGetUniformLocation(shader, "u_texTemplate")
        u_texTemplateResolution = glGetUniformLocation(shader, "u_texTemplateResolution")

    glUseProgram(shader)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
 
    # set uniform vec2f u_resolution after useProgram
    glUniform2f(u_resolution, WINDOW_WIDTH, WINDOW_HEIGHT)
    glUniform2f(u_mouse, 0, 0)
    glUniform1f(u_time, 0)
    if use_tex:
        glUniform1i(u_texTemplate, 0)
        glUniform2f(u_texTemplateResolution, textureWidth, textureHeight)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_QUADS, 0, 4)
    glFlush()
    glfw.swap_buffers(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
 
        glClear(GL_COLOR_BUFFER_BIT)
 
        # Draw Rectangle
        glDrawArrays(GL_QUADS, 0, 4)
 
        glfw.swap_buffers(window)

        outFile = path.splitext(path.split(fragFile)[-1])[0] + '.png'
        outBuffer = glReadPixels(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        print(len(outBuffer))
        outImage = Image.frombytes('RGBA', (WINDOW_WIDTH, WINDOW_HEIGHT), outBuffer)
        outImage = outImage.transpose(Image.FLIP_TOP_BOTTOM)
        outImage.save(outFile, 'PNG')
        break

    glfw.terminate()