import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Defining the 8 vertices for the cube in units
vertices = (
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
edges = (
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

def Cube():
    glBegin(GL_LINES)   # We are gonna make some lines
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])   # Specifying vertices
    glEnd()


pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -7)  # Zoom out

glRotatef(25, 1, 0, 0)

import serial

port = "COM3"

ser = serial.Serial(port, 115200, timeout=1)

delta_x = 0
delta_y = 0

current_x = 0
current_y = 0

while True:
    data = ser.readline()
    data_sensor = data.decode()
    angles = data_sensor.split(', ')
    if len(angles)==2:
        x_angle = float(angles[0])
        y_angle = float(angles[1])
        # x_angle = 45
        # y_angle = 45

        delta_x = x_angle - current_x
        delta_y = y_angle - current_y
        delta_z = 0 # We dont have that angle since we are using MPU6050

        # We convert the IMU axis to the pygame axis using rotation matrix
        glRotatef(delta_x, 1, 0, 0)
        glRotatef(delta_z, 0, 1, 0)
        glRotatef(-delta_y, 0, 0, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        current_x = x_angle
        current_y = y_angle
        print(x_angle, ' ', y_angle)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip() 
        pygame.time.wait(10)
    