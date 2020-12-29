import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import modelos
import lib.basic_shapes as bs
import lib.easy_shaders as es 
import lib.lightning_shaders as ls 
import lib.scene_graph2 as sg 
import transformations2 as tr 

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