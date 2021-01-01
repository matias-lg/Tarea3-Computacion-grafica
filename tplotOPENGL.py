# coding=utf-8
"""
Adaptacion de un ejemplo de los dados
Creditos a Daniel Calderon, CC3501, 2020-2
"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import transformations as tr
import easy_shaders as es
import basic_shapes as bs
import sys


# We will use 32 bits data, so an integer has 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')


# A simple class container to reference a shape on GPU memory
class GPUShape:
    vao = 0
    vbo = 0
    ebo = 0
    size = 0


def drawShape(shaderProgram, shape):

    # Binding the proper buffers
    glBindVertexArray(shape.vao)
    glBindBuffer(GL_ARRAY_BUFFER, shape.vbo)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, shape.ebo)

    # Describing how the data is stored in the VBO
    position = glGetAttribLocation(shaderProgram, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT,
                          GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shaderProgram, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE,
                          24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # This line tells the active shader program to render the active element buffer with the given size
    glDrawElements(GL_TRIANGLES, shape.size, GL_UNSIGNED_INT, None)

# Crea un grafico circular dados 4 porcentajes
def createTortaGraph(p1, p2, p3, p4):

    # Here the new shape will be stored
    gpuShape = GPUShape()
    lista = [0, 1, 0, 0.68, 0.68, 0.68]
    indicess = []

    r = 0.5

    delta = 10000
    # trozos de la circunferencia
    percent1 = delta * p1
    percent2 = delta * p2
    percent3 = delta * p3

    for i in range(0, delta):
        dt = 1 / delta
        # color azul | sanos
        if i <= percent1:
            lista += [r * np.cos(dt * i * np.pi * 2), r *
                      np.sin(dt * i * np.pi * 2) + 1, 0, 0, 0, 1]
        # color rojo | contagiados
        elif percent1 < i < percent1 + percent2:
            lista += [r * np.cos(dt * i * np.pi * 2), r *
                      np.sin(dt * i * np.pi * 2) + 1, 0, 1, 0, 0]
        # color amarillo | muertos
        elif percent1 + percent2 < i < percent1 + percent2 + percent3:
            lista += [r * np.cos(dt * i * np.pi * 2), r *
                      np.sin(dt * i * np.pi * 2) + 1, 0, 1, 1, 0]
        # color verde | inmune
        else:
            lista += [r * np.cos(dt * i * np.pi * 2), r *
                      np.sin(dt * i * np.pi * 2) + 1, 0, 0, 1, 0]
        # do not forget the indices!
        indicess += [0, i + 1, i + 2]

    # removing the last spare vertex
    indicess.pop()
    # Defining the location and colors of each vertex  of the shape
    vertexData = np.array(
        lista,
        dtype=np.float32)  # It is important to use 32 bits data

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(indicess, dtype=np.uint32)

    gpuShape.size = len(indices)

    # VAO, VBO and EBO and  for the shape
    gpuShape.vao = glGenVertexArrays(1)
    gpuShape.vbo = glGenBuffers(1)
    gpuShape.ebo = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, gpuShape.vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertexData) *
                 SIZE_IN_BYTES, vertexData, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gpuShape.ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) *
                 SIZE_IN_BYTES, indices, GL_STATIC_DRAW)

    return gpuShape

def draw(p1, p2, p3, p4):
    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(
        width, height, "Datos acumulados hasta el dia de Hoy", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)

    # shaders a usar
    pipeline = es.SimpleTransformShaderProgram()
    pipeline_tex = es.SimpleTextureTransformShaderProgram()
    # matrices
    transform1 = np.matmul(tr.scale(1, 0.5, 0), tr.translate(0, 1.5, 0))
    transform2 = tr.translate(0, -1, 0)
    # textura de la leyenda
    imagen = es.toGPUShape(bs.createTextureQuad(
        "img/leyenda.png", 1, 1), GL_REPEAT, GL_NEAREST)

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(1.0, 1.0, 1.0, 1.0)

    torta = createTortaGraph(p1, p2, p3, p4)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        # Texturas con fondos transparentes
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Shader de textura y dibujar
        glUseProgram(pipeline_tex.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(
            pipeline_tex.shaderProgram, "transform"), 1, GL_TRUE, transform1)
        pipeline_tex.drawShape(imagen)

        # Cambiar shaders y dibujar grafico de torta
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(
            pipeline.shaderProgram, "transform"), 1, GL_TRUE, transform2)
        drawShape(pipeline.shaderProgram, torta)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
