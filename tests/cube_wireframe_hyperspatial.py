import random
import pygame
import time

from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define vertices and edges for a cube
vertices = [
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
]

# Initialize Pygame and create a window
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Enable depth test
glEnable(GL_DEPTH_TEST)

# Define the initial position and velocity for the x-axis
x_position = 0.0
x_velocity = 0.01  # Adjust the speed as necessary

# Initialize the position and velocity of the cube
position = [0.0, 0.0, -5.0]

# Define the velocity more precisely
velocity = [1.5, 1.5, 0.0]  # Units per second for x, y, z

# Define the boundary limits for the cube's movement
x_limit = 2.0
y_limit = 1.5

# Define rotation speed and initialize the rotation angle
rotation_speed = 90.0  # Degrees per second

# Define an angle of rotation
angle = 0.0

# Create a clock object to manage the frame rate
clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Calculate delta time
    delta_time = clock.tick(60) / 1000.0  # Limit to 60 frames per second, convert to seconds

    # Update the position based on the velocity and delta time
    position[0] += velocity[0] * delta_time
    position[1] += velocity[1] * delta_time

    # Boundary checks with position adjustment
    if position[0] > x_limit or position[0] < -x_limit:
        position[0] = x_limit if position[0] > x_limit else -x_limit
        velocity[0] = -velocity[0]
    if position[1] > y_limit or position[1] < -y_limit:
        position[1] = y_limit if position[1] > y_limit else -y_limit
        velocity[1] = -velocity[1]

    # Update the angle for rotation based on rotation speed and delta time
    angle += rotation_speed * delta_time

    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(*position)

    # Rotate the cube
    glRotatef(angle, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the wireframe cube without colors
    glBegin(GL_LINES)
    for edge in vertices:
        for vertex in vertices:
            glVertex3fv(edge)
            glVertex3fv(vertex)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)