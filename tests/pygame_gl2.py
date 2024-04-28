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

# Define the faces using vertices
faces = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
]

# Define color for each face
colors = [
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Cyan
]

# At the start, after defining the original colors
original_colors = list(colors)  # Make a copy of the original colors
gradient_colors = list(colors)  # This will store the gradient colors upon collision

# Initialize Pygame and create a window
pygame.init()
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Set perspective
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Enable color material and depth test
glEnable(GL_DEPTH_TEST)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

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

# Define the last time variable
last_time = pygame.time.get_ticks()

# Create a clock object to manage the frame rate
clock = pygame.time.Clock()

def get_random_color():
    return (random.random(), random.random(), random.random())

def interpolate_color(color1, color2, t):
    # Interpolate between two colors. 't' is a value between 0 and 1.
    return tuple(a + (b - a) * t for a, b in zip(color1, color2))

def interpolate_vertex_colors(original_vertex_colors, target_vertex_colors, t):
    return [interpolate_color(orig, target, t) for orig, target in zip(original_vertex_colors, target_vertex_colors)]

# A simple non-linear interpolation for more dynamic effect.
def non_linear_interpolate(start, end, t):
    t = t * t  # Square the parameter to create a non-linear transition
    return interpolate_color(start, end, t)

last_collision_time = 0
fade_duration = 1.0  # Adjust this duration as needed

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

    # Variable to track if a collision occurred
    collision_occurred = False

    # Boundary checks with position adjustment
    if position[0] > x_limit or position[0] < -x_limit:
        position[0] = x_limit if position[0] > x_limit else -x_limit
        velocity[0] = -velocity[0]
        collision_occurred = True
    if position[1] > y_limit or position[1] < -y_limit:
        position[1] = y_limit if position[1] > y_limit else -y_limit
        velocity[1] = -velocity[1]
        collision_occurred = True

    # Update the angle for rotation based on rotation speed and delta time
    angle += rotation_speed * delta_time

    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(*position)

    if collision_occurred:
        last_collision_time = current_time
        new_colors = [get_random_color() for _ in original_colors]  # Get new random colors for each face
        for i in range(len(faces)):
            gradient_colors[i] = interpolate_color(original_colors[i], new_colors[i], 0.5)  # Blend old and new colors
        original_colors = new_colors  # Update original colors

    # Rotate the cube
    glRotatef(angle, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Update last_collision_time and store gradient colors on collision
    current_time = time.time()

    # Calculate the fade factor
    time_since_collision = current_time - last_collision_time
    fade_factor = min(time_since_collision / fade_duration, 1)

    # Draw the cube with interpolated colors for each vertex
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        if fade_factor < 1.0:
            color = interpolate_color(gradient_colors[i], original_colors[i], fade_factor)
        else:
            color = original_colors[i]
        
        glColor3fv(color)
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)