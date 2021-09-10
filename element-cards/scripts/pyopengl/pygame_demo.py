from only_frag import WINDOW_HEIGHT, WINDOW_WIDTH
from OpenGL.GL import *
from OpenGL.GL.shaders import *

import pygame
from pygame.locals import *
import numpy
import time
import sys

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 640


def getFileContent(file):
    content = open(file, 'r').read()
    return content


def init():
    pygame.init()

    global WINDOW_WIDTH, WINDOW_HEIGHT
    global imgsize
    img = pygame.image.load("tarot-merge.png")
    textureData = pygame.image.tostring(img, "RGBA", 1)
    imgsize = (img.get_width(), img.get_height())
    WINDOW_WIDTH, WINDOW_HEIGHT = imgsize

    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                            HWSURFACE | OPENGL | DOUBLEBUF)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    # textureData = pygame.image.tostring(img, "RGBA")

    global texID
    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texID)

    # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 4,
                 imgsize[0], imgsize[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    vertices = [-1.0, -1.0,
                -1.0, 1.0,
                1.0, 1.0,
                1.0, -1.0]

    vertices = numpy.array(vertices, dtype=numpy.float32)

    vertexShader = compileShader(getFileContent(
        "pygame_demo.vert"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContent(
        "pygame_demo.frag"), GL_FRAGMENT_SHADER)

    global shaderProgram
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)
    glLinkProgram(shaderProgram)

    v_vertices = glGetAttribLocation(shaderProgram, 'vPosition')
    glVertexAttribPointer(v_vertices, 2, GL_FLOAT, GL_FALSE, 0, vertices)
    glEnableVertexAttribArray(v_vertices)

    global texLocation
    texLocation = glGetUniformLocation(shaderProgram, "u_texTemplate")
    global u_texSize
    u_texSize = glGetUniformLocation(shaderProgram, "u_texTemplateResolution")
    global u_resolution
    u_resolution = glGetUniformLocation(shaderProgram, "u_resolution")


def main():
    init()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        glClearColor(0., 0., 0., 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shaderProgram)
        global texLocation, texID
        glUniform1i(texLocation, 0)
        global u_texSize
        glUniform2f(u_texSize, imgsize[0], imgsize[1])
        global u_resolution
        global WINDOW_WIDTH, WINDOW_HEIGHT
        glUniform2f(u_resolution, WINDOW_WIDTH, WINDOW_HEIGHT)
        glDrawArrays(GL_QUADS, 0, 4)

        pygame.display.flip()


main()
