import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random  # Import the random module

# Define the dimensions of the main cube
main_cube_size = 2.0  # Reduced size for the main cube
main_cube_speed = 0.02  # Adjust the speed as needed

# Define the dimensions of the Rubik's Cube
cube_size = 10  # Number of small cubes per side
cube_spacing = 1.2  # Increased spacing to avoid overlap

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

# Initialize the position and velocity of the main cube
main_cube_x, main_cube_y, main_cube_z = 0.0, 0.0, 0.0
main_cube_vel_x, main_cube_vel_y, main_cube_vel_z = (
    main_cube_speed,
    main_cube_speed,
    main_cube_speed,
)

# Rotation angles
angle_x, angle_y, angle_z = 0.0, 0.0, 0.0
rotation_speed = 1.0  # Adjust rotation speed as needed

# Function to generate a random color
def random_color():
    return (random.random(), random.random(), random.random())

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    # Update the position of the main cube
    main_cube_x += main_cube_vel_x
    main_cube_y += main_cube_vel_y
    main_cube_z += main_cube_vel_z

    # Bounce the main cube off the borders
    if (
        main_cube_x + main_cube_size / 2 > 10.0
        or main_cube_x - main_cube_size / 2 < -10.0
    ):
        main_cube_vel_x *= -1

    if (
        main_cube_y + main_cube_size / 2 > 10.0
        or main_cube_y - main_cube_size / 2 < -10.0
    ):
        main_cube_vel_y *= -1

    if (
        main_cube_z + main_cube_size / 2 > 10.0
        or main_cube_z - main_cube_size / 2 < -10.0
    ):
        main_cube_vel_z *= -1

    # Rotate the entire Rubik's Cube
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    # Draw the main cube
    glPushMatrix()
    glTranslatef(main_cube_x, main_cube_y, main_cube_z)
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glutSolidCube(main_cube_size)
    glPopMatrix()

    # Draw the Rubik's Cube by creating solid small cubes with random colors
    for x in range(-cube_size // 2, cube_size // 2):
        for y in range(-cube_size // 2, cube_size // 2):
            for z in range(-cube_size // 2, cube_size // 2):
                # Translate to the position of the small cube
                glPushMatrix()
                glTranslatef(x * step, y * step, z * step)

                # Draw the small cube with vertices for all six faces and a random color
                color = random_color()
                glColor3fv(color)
                glBegin(GL_QUADS)

                # Front face
                glVertex3f(-0.5, -0.5, 0.5)
                glVertex3f(0.5, -0.5, 0.5)
                glVertex3f(0.5, 0.5, 0.5)
                glVertex3f(-0.5, 0.5, 0.5)

                # Back face
                glVertex3f(-0.5, -0.5, -0.5)
                glVertex3f(0.5, -0.5, -0.5)
                glVertex3f(0.5, 0.5, -0.5)
                glVertex3f(-0.5, 0.5, -0.5)

                # Top face
                glVertex3f(-0.5, 0.5, 0.5)
                glVertex3f(0.5, 0.5, 0.5)
                glVertex3f(0.5, 0.5, -0.5)
                glVertex3f(-0.5, 0.5, -0.5)

                # Bottom face
                glVertex3f(-0.5, -0.5, 0.5)
                glVertex3f(0.5, -0.5, 0.5)
                glVertex3f(0.5, -0.5, -0.5)
                glVertex3f(-0.5, -0.5, -0.5)

                # Left face
                glVertex3f(-0.5, 0.5, 0.5)
                glVertex3f(-0.5, -0.5, 0.5)
                glVertex3f(-0.5, -0.5, -0.5)
                glVertex3f(-0.5, 0.5, -0.5)

                # Right face
                glVertex3f(0.5, 0.5, 0.5)
                glVertex3f(0.5, -0.5, 0.5)
                glVertex3f(0.5, -0.5, -0.5)
                glVertex3f(0.5, 0.5, -0.5)

                glEnd()

                glPopMatrix()

    glPopMatrix()

    # Increment the rotation angles
    angle_x += rotation_speed
    angle_y += rotation_speed
    angle_z += rotation_speed

    pygame.display.flip()
    pygame.time.wait(10)