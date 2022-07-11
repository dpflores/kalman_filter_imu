from asyncore import write
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


import os

DATA_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "\data"
DATA_FILE = os.path.dirname(os.path.realpath(__file__)) + "\data\data.txt"

def write_to_file(dt, wx, wy, wz, ax, ay, az):
    
    with open(DATA_FILE, 'a') as file:
        file.write(str(dt) + ", " + str(wx) + ", " + str(wy) + ", " + str(wz) + ", " + str(ax) + ", " + str(ay) + ", " + str(az) + "\n")
        file.close()


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

if not os.path.exists(DATA_FOLDER):
  
  # Create a new directory because it does not exist 
  os.makedirs(DATA_FOLDER)
  print("The new directory is created!")
  
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
    data_sensor = data_sensor.split(', ')
    if len(data_sensor)==7:
        dt = float(data_sensor[0])
        ax = float(data_sensor[1])
        ay = float(data_sensor[2])
        az = float(data_sensor[3])
        wx = float(data_sensor[4])
        wy = float(data_sensor[5])
        wz = float(data_sensor[6])
        
        write_to_file(dt, wx, wy, wz, ax, ay, az)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

        # current_x = x_angle
        # current_y = y_angle
        # print(x_angle, ' ', y_angle)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip() 
        pygame.time.wait(10)
    