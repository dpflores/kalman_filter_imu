from asyncore import write
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class RectangularPrism:
    def __init__(self):
        # Defining the 8 vertices for the cube in units
        self.vertices = (
            (1, -0.5, -2),
            (1, 0.5, -2),
            (-1, 0.5, -2),
            (-1, -0.5, -2),
            (1, -0.5, 2),
            (1, 0.5, 2),
            (-1, -0.5, 2),
            (-1, 0.5, 2)
        )
        # Defining the 12 edges of the cube that connects the vertices
        self.edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7)
        )
    
    def write_prism(self):
        glBegin(GL_LINES)   # We are gonna make some lines
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])   # Specifying vertices
        glEnd()

    def show_prism(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.write_prism()
        pygame.display.flip() 
        pygame.time.wait(10)
    
    def setup_display(self):
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

        glTranslatef(0.0, 0.0, -7)  # Zoom out

        glRotatef(25, 1, 0, 0)