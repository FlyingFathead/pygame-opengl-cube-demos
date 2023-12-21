# "Cube Libre" v0.03
#
# By FlyingFathead (w/ a little help from digital friends) // Dec 2023
# https://github.com/FlyingFathead
#
# changelog:
# v.0.03 - horizon, navigation
# v.0.02 - solid color

import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Define the dimensions of the main cube
cube_size = 10  # Number of small cubes per side
cube_spacing = 1.0  # Increased spacing to avoid overlap

# Calculate the step size for positioning small cubes
step = cube_spacing

# Initialize Pygame and create a window
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Set perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20.0)  # Move the view farther back

# Define the vertices for a cube
vertices = [
    # Front face
    -0.5, -0.5, 0.5,
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,
    -0.5, 0.5, 0.5,

    # Back face
    0.5, -0.5, -0.5,
    -0.5, -0.5, -0.5,
    -0.5, 0.5, -0.5,
    0.5, 0.5, -0.5,

    # Top face
    -0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, -0.5,
    -0.5, 0.5, -0.5,

    # Bottom face
    -0.5, -0.5, 0.5,
    0.5, -0.5, 0.5,
    0.5, -0.5, -0.5,
    -0.5, -0.5, -0.5,

    # Left face
    -0.5, -0.5, 0.5,
    -0.5, 0.5, 0.5,
    -0.5, 0.5, -0.5,
    -0.5, -0.5, -0.5,

    # Right face
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, -0.5,
    0.5, -0.5, -0.5,
]

# Create a VBO to store the vertex data
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

# Create a VAO to store the vertex attribute configuration
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# Specify vertex attribute pointers
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

# Unbind the VAO and VBO
glBindVertexArray(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)

# Initialize rotation angles
angle_x, angle_y, angle_z = 0.0, 0.0, 0.0
rotation_speed = 1.0  # Adjust rotation speed as needed

# Define a function to generate random RGB colors
def random_color():
    return [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.color = self.random_color()  # Assign a random color at creation
        self.is_destroyed = False

    @staticmethod
    def random_color():
        return [random.uniform(0, 1) for _ in range(3)]

    # Add other necessary methods and attributes

# Initialize cubes
cube_size = 5  # Adjust as necessary
cubes = [[[Cube(x, y, z) for z in range(-cube_size // 2, cube_size // 2)] 
          for y in range(-cube_size // 2, cube_size // 2)] 
         for x in range(-cube_size // 2, cube_size // 2)]

# Movement speed
move_speed = 0.1

def draw_wireframe_horizon():
    glColor3f(1.0, 1.0, 1.0)  # White color
    glLineWidth(1)  # Set line width
    glBegin(GL_LINES)

    # Horizontal lines
    for z in range(-20, 21, 2):  # Adjust range and step for density
        glVertex3f(-20, -5, z)  # Adjust Y-coordinate for vertical position
        glVertex3f(20, -5, z)

    # Vertical lines
    for x in range(-20, 21, 2):  # Adjust range and step for density
        glVertex3f(x, -5, -20)  # Starting from far distance
        glVertex3f(x, -5, 20)   # Up to close distance

    glEnd()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Handle keyboard events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        for row in cubes:
            for layer in row:
                for cube in layer:
                    cube.x -= move_speed
    if keys[pygame.K_RIGHT]:
        for row in cubes:
            for layer in row:
                for cube in layer:
                    cube.x += move_speed
    if keys[pygame.K_UP]:
        for row in cubes:
            for layer in row:
                for cube in layer:
                    cube.y += move_speed
    if keys[pygame.K_DOWN]:
        for row in cubes:
            for layer in row:
                for cube in layer:
                    cube.y -= move_speed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    # Inside your main game loop, before drawing the cubes:
    draw_wireframe_horizon()

    # Rotate the entire cube
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    for x in range(-cube_size // 2, cube_size // 2):
        for y in range(-cube_size // 2, cube_size // 2):
            for z in range(-cube_size // 2, cube_size // 2):
                cube = cubes[x][y][z]

                glPushMatrix()
                glTranslatef(cube.x * step, cube.y * step, cube.z * step)
                glColor3fv(cube.color)  # Use the cube's assigned color

                # Draw the cube using the VAO and VBO
                glBindVertexArray(vao)
                glDrawArrays(GL_QUADS, 0, 24)  # Assuming 24 vertices for a cube
                glBindVertexArray(0)

                glPopMatrix()

    glPopMatrix()

    angle_x += rotation_speed
    angle_y += rotation_speed
    angle_z += rotation_speed

    pygame.display.flip()
    pygame.time.wait(10)
