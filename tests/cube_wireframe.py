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
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Set perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0,0.0, -5)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # Draw the polygon
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)