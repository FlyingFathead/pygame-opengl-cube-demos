import random
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Voxel:
    def __init__(self, position, size=0.1):
        self.position = position
        self.size = size
        self.active = True

    def get_vertices(self):
        x, y, z = self.position
        s = self.size / 2
        return [
            (x - s, y - s, z - s),
            (x + s, y - s, z - s),
            (x + s, y + s, z - s),
            (x - s, y + s, z - s),
            (x - s, y - s, z + s),
            (x + s, y - s, z + s),
            (x + s, y + s, z + s),
            (x - s, y + s, z + s)
        ]

def create_voxel_cube(cube_size, voxel_size):
    voxels = []
    offset = cube_size * voxel_size / 2
    for x in range(cube_size):
        for y in range(cube_size):
            for z in range(cube_size):
                voxel_position = (x * voxel_size - offset, y * voxel_size - offset, z * voxel_size - offset)
                voxels.append(Voxel(voxel_position, voxel_size))
    return voxels

def get_random_color():
    return (random.random(), random.random(), random.random())

def interpolate_color(color1, color2, t):
    return tuple(a + (b - a) * t for a, b in zip(color1, color2))

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -25)

# Cube settings
x_limit = 5
y_limit = 5
velocity = [0.1, 0.1, 0.0]
position = [0.0, 0.0, 0.0]
rotation_speed = 90.0
angle = 0.0
last_time = pygame.time.get_ticks()
fade_duration = 1.0
last_collision_time = 0

# Create voxel cube
voxel_cube = create_voxel_cube(10, 0.5)  # 10x10x10 cube of voxels
original_colors = [get_random_color() for _ in voxel_cube]
gradient_colors = list(original_colors)

# Main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Calculate delta time
    delta_time = clock.tick(60) / 1000.0

    # Update position and check for collision
    position[0] += velocity[0] * delta_time
    position[1] += velocity[1] * delta_time
    collision_occurred = False
    if position[0] > x_limit or position[0] < -x_limit or position[1] > y_limit or position[1] < -y_limit:
        collision_occurred = True
        velocity[0] *= -1 if position[0] > x_limit or position[0] < -x_limit else 1
        velocity[1] *= -1 if position[1] > y_limit or position[1] < -y_limit else 1
        # Remove a random voxel
        random.choice(voxel_cube).active = False

    # Rotate the cube
    angle += rotation_speed * delta_time
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(*position)
    glRotatef(angle, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the cube
    glBegin(GL_QUADS)
    for voxel, color in zip(voxel_cube, gradient_colors):
        if voxel.active:
            vertices = voxel.get_vertices()
            for vertex in vertices:
                glColor3fv(color)
                glVertex3fv(vertex)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)