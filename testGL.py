import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import json
from modelos import *
import basic_shapes as bs
import easy_shaders as es 
import scene_graph2 as sg 
import transformations2 as tr
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

# obtener data 
with open("virus.json") as f:
    data = json.load(f)
inputs = data[0]
radius = inputs['Radius']
cont_prob = inputs['Contagious_prob']
death_rate = inputs['Death_rate']
poblacion = inputs['Initial_population']
heal_days = inputs['Days_to_heal']
cnt = 0
dia = 0
sim = Simulator(radius, cont_prob, death_rate, poblacion, heal_days)
dias = []
normales = []
contagios = []
recuperados = []
muertos = []
print('Simulando...')
while True:
    #  graficar
    sanos = sim._sim.getPositions()
    enfermos = sim._sim.getInfectedPositions()
    # Simulamos el dia actual
    data = sim.Simulate()
    # actualiza arreglos para el otro grafico
    dia += 1
    dias.append(dia)
    normales.append(data[3])
    contagios.append(data[4])
    recuperados.append(data[5])
    muertos.append(data[6])
    # actualizamos posiciones / estados
    sim._sim.update()
    # informacion en consola
    if len(enfermos) == 0:
        cnt += 1
    if cnt > heal_days + 1:
        break

if __name__ == '__main__':

    # Initialize glfw  
    if not glfw.init():
        sys.exit()

    width = 800
    height = 800

    window = glfw.create_window(width, height, 'Plot', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

   
    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colores


    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Filling or not the shapes depending on the controller state
        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()