import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define vertices and edges for a cube
vertices = [
    (1, -1, -1),  # Vertex 0
    (1, 1, -1),   # Vertex 1
    (-1, 1, -1),  # Vertex 2
    (-1, -1, -1), # Vertex 3
    (1, -1, 1),   # Vertex 4
    (1, 1, 1),    # Vertex 5
    (-1, -1, 1),  # Vertex 6
    (-1, 1, 1)    # Vertex 7
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Edges of the bottom face
    (4, 5), (5, 7), (7, 6), (6, 4),  # Edges of the top face
    (0, 4), (1, 5), (2, 7), (3, 6)   # Edges connecting the top and bottom faces
]

# Initialize Pygame and create a window
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Set initial position and velocity
x, y, z = 0.0, 0.0, 0.0
vx, vy, vz = 0.02, 0.03, 0.04

# Set boundary limits
x_limit, y_limit, z_limit = 1.0, 1.0, 1.0

# Rotation angles
angle_x, angle_y, angle_z = 0.0, 0.0, 0.0
rotation_speed = 1.0  # Adjust rotation speed as needed

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    x += vx
    y += vy
    z += vz

    # Bounce off the edges
    if x > x_limit or x < -x_limit:
        vx *= -1
    if y > y_limit or y < -y_limit:
        vy *= -1
    if z > z_limit or z < -z_limit:
        vz *= -1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glTranslatef(x, y, z)

    # Rotate the cube on its axis
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    # Increment the rotation angles
    angle_x += rotation_speed
    angle_y += rotation_speed
    angle_z += rotation_speed

    # Draw the polygon
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)