# "Cube Libre" v0.12
#
# By FlyingFathead (w/ a little help from imaginary digital friends)
# // Created and updated: Dec 2023, Oct 2024
# https://github.com/FlyingFathead/pygame-opengl-polygon-demos
#
version_number = "0.12.6"

import os
import pygame

from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *

import random

# Detect if running under Wayland
is_wayland = 'WAYLAND_DISPLAY' in os.environ

# Set environment variables based on the detected windowing system
if is_wayland:
    # Attempt to use native Wayland support if available
    print("[INFO] Detected Wayland. Attempting to use native Wayland support.")
    # Potentially set other SDL environment variables here if needed
else:
    # Default to X11
    print("[INFO] Using X11 as the windowing system.")

# Define the dimensions of the main cube
cube_size = 5  # Number of small cubes per side
cube_spacing = 1.0  # Increased spacing to avoid overlap

# Calculate the step size for positioning small cubes
step = cube_spacing

# Movement speed
move_speed = 5.0  # Increased for more noticeable movement
z_move_speed = 5.0  # Define Z-axis movement speed

# *** Begin Portal Properties ***
portal_position = (0.0, 0.0, 20.0)  # Position of the portal (x, y, z)
portal_size = 5.0  # Width and height of the portal
portal_color = (0.0, 1.0, 1.0)  # Cyan color for glowing effect
portal_glow_steps = 10  # Number of overlapping quads for the glow effect
portal_glow_alpha = 0.3  # Initial alpha for the glow
# *** End Portal Properties ***

# *** Begin Animation States ***
is_animating = False
animation_duration = 2.0  # Duration of the zoom animation in seconds
animation_timer = 0.0
animation_scale = 1.0  # Current scale factor for animation
# *** End Animation States ***

# Initialize Pygame and create a window
pygame.init()
display = (800, 600)

# Using numerical value for compatibility profile
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, 0x00002)

# Request OpenGL 3.3 compatibility profile
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)

try:
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
except pygame.error as e:
    print(f"Pygame failed to set display mode with OpenGL: {e}")
    pygame.quit()
    quit()

# Set the window title with version number
pygame.display.set_caption(f"Cube Libre (demo, v.{version_number})")

# Verify OpenGL version
version = glGetString(GL_VERSION)
if version:
    version_string = version.decode()
    print(f"OpenGL version: {version_string}")
    
    # Extract major and minor version numbers
    version_parts = version_string.split(' ')[0]
    major_minor = version_parts.split('.')[:2]
    
    try:
        major, minor = map(int, major_minor)
    except ValueError:
        print(f"Unexpected OpenGL version format: {version_string}")
        pygame.quit()
        quit()
    
    if major < 3:
        print("OpenGL version is below 3.0. VAOs and VBOs may not be supported.")
        pygame.quit()
        quit()
else:
    print("Failed to retrieve OpenGL version.")
    pygame.quit()
    quit()

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Set perspective and translate
try:
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -30.0)  # Move the view farther back
except OpenGL.error.GLError as e:
    print(f"OpenGL Error during gluPerspective or glTranslatef: {e}")
    pygame.quit()
    quit()

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

# *** Create a VBO to store the vertex data ***
try:
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)
except OpenGL.error.GLError as e:
    print(f"OpenGL Error during VBO setup: {e}")
    pygame.quit()
    quit()

# *** Create a VAO to store the vertex attribute configuration ***
try:
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # Specify vertex attribute pointers
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    # Unbind the VAO and VBO
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
except OpenGL.error.GLError as e:
    print(f"OpenGL Error during VAO/VBO setup: {e}")
    pygame.quit()
    quit()

# Initialize rotation angles
angle_x, angle_y, angle_z = 0.0, 0.0, 0.0
rotation_speed = 20.0  # Degrees per second for smoother rotation

# Initialize the clock for managing delta_time
clock = pygame.time.Clock()

# Define a function to generate random RGB colors
def random_color():
    return [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

# Cube class with the destroy method restored to original behavior
class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.color = self.random_color()
        self.is_destroyed = False
        self.flash_duration = 0.2  # Duration of flash effect in seconds
        self.time_since_destroyed = 0  # Time since the cube was destroyed
        self.rotation = 0.0
        # Restore original fly-off velocity 
        self.velocity = [0.0, 0.0, 0.0]

    @staticmethod
    def random_color():
        return [random.uniform(0, 1) for _ in range(3)]

    def destroy(self):
        print("Destroying cube")  # Debugging statement        
        self.color = [0.8, 0.8, 0.8]  # Flash effect on destruction
        # Set original fly-off velocities
        self.velocity = [random.uniform(-1, 1), random.uniform(1, 2), random.uniform(-1, 1)]
        self.angular_velocity = random.uniform(-3, 3) # Degrees per second
        self.is_destroyed = True
        self.time_since_destroyed = 0  # Reset timer on destruction
    
    # Reset animation state for restart
    def reset_animation_state(self):
        self.x, self.y, self.z = self.initial_x, self.initial_y, self.initial_z
        self.color = self.random_color()
        self.is_destroyed = False
        self.velocity = [0.0, 0.0, 0.0]
        self.angular_velocity = 0.0
        self.rotation = 0.0

# Initialize cubes
cubes = [[[Cube(x, y, z) for z in range(-cube_size // 2, cube_size // 2)] 
          for y in range(-cube_size // 2, cube_size // 2)] 
         for x in range(-cube_size // 2, cube_size // 2)]

# Define the portal boundaries for collision detection
portal_half_size = portal_size / 2
portal_bounds = {
    'x_min': portal_position[0] - portal_half_size,
    'x_max': portal_position[0] + portal_half_size,
    'y_min': portal_position[1] - portal_half_size,
    'y_max': portal_position[1] + portal_half_size,
    'z_min': portal_position[2] - portal_half_size,
    'z_max': portal_position[2] + portal_half_size,
}

# Assuming the horizon is at a fixed Y-coordinate
horizon_y = -5

# Define the number of stars
num_stars = 1000

# Generate random positions for stars
stars = [(random.uniform(-50, 50), random.uniform(-50, 50), random.uniform(-50, 50)) for _ in range(num_stars)]

def draw_stars():
    glPointSize(2)  # Adjust point size for visibility
    glBegin(GL_POINTS)
    for star in stars:
        glVertex3fv(star)
    glEnd()

# Horizon collision detection (based on Y-axis)
def check_collision_with_horizon(cube):
    if cube.y <= horizon_y:
        print(f"Collision detected with horizon for cube at ({cube.x:.2f}, {cube.y:.2f}, {cube.z:.2f})")
        return True
    return False

# Portal collision detection (based on Z-axis)
def check_collision_with_portal(cube):
    # Define cube's position
    cube_pos = (cube.x * step, cube.y * step, cube.z * step)
    
    # Check if cube is within the portal's X and Y bounds
    within_x = portal_bounds['x_min'] <= cube_pos[0] <= portal_bounds['x_max']
    within_y = portal_bounds['y_min'] <= cube_pos[1] <= portal_bounds['y_max']
    
    # Check if cube has reached the portal's Z position (with a small threshold)
    reached_z = portal_bounds['z_min'] <= cube_pos[2] <= portal_bounds['z_max']
    
    if within_x and within_y and reached_z:
        print(f"Collision detected with portal for cube at position ({cube.x:.2f}, {cube.y:.2f}, {cube.z:.2f})")
        return True
    return False

# Update cube positions based on velocity
def update_cubes(delta_time):
    global screen_shake_timer, flash_timer
    if flash_timer > 0:
        flash_timer -= delta_time    
    for x in range(-cube_size // 2, cube_size // 2):
        for y in range(-cube_size // 2, cube_size // 2):
            for z in range(-cube_size // 2, cube_size // 2):
                cube = cubes[x][y][z]
                if cube.is_destroyed:
                    cube.time_since_destroyed += delta_time
                    if cube.time_since_destroyed > cube.flash_duration:
                        # Update positions based on velocity
                        cube.x += cube.velocity[0] * delta_time
                        cube.y += cube.velocity[1] * delta_time
                        cube.z += cube.velocity[2] * delta_time
                        cube.rotation += cube.angular_velocity * delta_time  # Update rotation

# Draw the wireframe horizon
def draw_wireframe_horizon():
    glColor3f(1.0, 1.0, 1.0)  # White color
    glLineWidth(1)  # Set line width
    glBegin(GL_LINES)

    # Horizontal lines
    for z in range(-50, 51, 5):  # Adjust range and step for density
        glVertex3f(-50, horizon_y, z)  # Adjust Y-coordinate for vertical position
        glVertex3f(50, horizon_y, z)

    # Vertical lines
    for x in range(-50, 51, 5):  # Adjust range and step for density
        glVertex3f(x, horizon_y, -50)  # Starting from far distance
        glVertex3f(x, horizon_y, 50)   # Up to close distance

    glEnd()

def gradient_color(y):
    # Assuming the vertical range is from -cube_size/2 to cube_size/2
    gradient_start = [1, 0, 0] # Red at the top
    gradient_end = [0, 0, 1] # Blue at the bottom
    factor = (y + cube_size/2) / cube_size # Normalize y to range [0, 1]
    color = [
        gradient_start[0] * (1 - factor) + gradient_end[0] * factor,
        gradient_start[1] * (1 - factor) + gradient_end[1] * factor,
        gradient_start[2] * (1 - factor) + gradient_end[2] * factor
    ]
    return color

def draw_scene(animation_scale=1.0):
    # Rendering
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    # Apply scaling for animation
    glScalef(animation_scale, animation_scale, animation_scale)

    # Rotate the entire scene
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    # Draw wireframe horizon
    draw_wireframe_horizon()

    # Draw stars
    glColor3f(1, 1, 1)  # White stars
    draw_stars()

    # *** Enable blending for transparency if any cubes are destroyed ***
    if any(cube.is_destroyed for row in cubes for layer in row for cube in layer):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Apply gradient in the cube rendering loop
    for x in range(-cube_size // 2, cube_size // 2):
        for y in range(-cube_size // 2, cube_size // 2):
            for z in range(-cube_size // 2, cube_size // 2):
                cube = cubes[x][y][z]
                glPushMatrix()
                glTranslatef(cube.x * step, cube.y * step, cube.z * step)
                if cube.is_destroyed:
                    # *** Preserve original color and apply transparency ***
                    glColor4f(*cube.color, 0.5)  # Original color with alpha
                else:
                    gradient_color_value = gradient_color(cube.y)
                    glColor3fv(gradient_color_value)
                glBindVertexArray(vao)
                glDrawArrays(GL_QUADS, 0, 24)
                glBindVertexArray(0)
                glPopMatrix()

    # *** Disable blending after drawing cubes ***
    if any(cube.is_destroyed for row in cubes for layer in row for cube in layer):
        glDisable(GL_BLEND)

    # *** Begin Portal Rendering ***
    draw_portal()
    # *** End Portal Rendering ***
    
    glPopMatrix()

# Draw the portal
def draw_portal():
    glPushMatrix()
    glTranslatef(*portal_position)
    
    # Enable blending for the glowing effect
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Draw the main portal quad
    glColor4f(*portal_color, 1.0)  # Full opacity for the main portal
    glBegin(GL_QUADS)
    half_size = portal_size / 2
    glVertex3f(-half_size, -half_size, 0.0)
    glVertex3f(half_size, -half_size, 0.0)
    glVertex3f(half_size, half_size, 0.0)
    glVertex3f(-half_size, half_size, 0.0)
    glEnd()
    
    # Create a glowing effect by drawing larger, semi-transparent quads
    for i in range(1, portal_glow_steps + 1):
        scale = 1.0 + (i * 0.2)  # Increase size for each glow layer
        alpha = portal_glow_alpha / i  # Decrease alpha for each layer
        glColor4f(*portal_color, alpha)
        glPushMatrix()
        glScalef(scale, scale, scale)
        glBegin(GL_QUADS)
        glVertex3f(-half_size, -half_size, 0.0)
        glVertex3f(half_size, -half_size, 0.0)
        glVertex3f(half_size, half_size, 0.0)
        glVertex3f(-half_size, half_size, 0.0)
        glEnd()
        glPopMatrix()
    
    glDisable(GL_BLEND)
    glPopMatrix()

def all_cubes_destroyed(cubes):
    return all(cube.is_destroyed for row in cubes for layer in row for cube in layer)

def reset_cubes(cubes):
    # Logic to reset the cubes to their initial state
    print("Resetting all cubes to initial state.")
    for x in range(-cube_size // 2, cube_size // 2):
        for y in range(-cube_size // 2, cube_size // 2):
            for z in range(-cube_size // 2, cube_size // 2):
                cubes[x][y][z].reset_animation_state()
                print(f"Cube at ({cubes[x][y][z].x:.2f}, {cubes[x][y][z].y:.2f}, {cubes[x][y][z].z:.2f}) has been reset.")

# Flash the screen
def flash_screen(duration=1000, steps=255):
    # Duration of the flash in milliseconds
    # Steps are how many levels of fading we have

    # Fade to white
    for i in range(steps):
        alpha = i / steps
        glClearColor(alpha, alpha, alpha, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_scene()
        pygame.display.flip()
        pygame.time.wait(duration // (steps * 2))  # Wait proportionally to fade duration

    # Hold the white screen
    pygame.time.wait(duration // steps)  # Hold the white screen for a moment

    # Fade back into the game
    for i in range(steps, -1, -1):
        alpha = i / steps
        glClearColor(alpha, alpha, alpha, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_scene()  # Draw the game scene with the faded alpha overlay
        pygame.display.flip()
        pygame.time.wait(duration // (steps * 2))  # Wait proportionally to fade duration

    # Reset clear color to game's background color
    glClearColor(0, 0, 0, 1)  # Assuming black is the game's background color

# Additional global variables for effects
screen_shake_duration = 0.5  # Duration of the shake in seconds
screen_shake_timer = 0  # Current shake timer
flash_duration = 0.3  # Duration of the flash in seconds
flash_timer = 0  # Current flash timer

def trigger_hit_effects():
    global screen_shake_timer, flash_timer
    screen_shake_timer = screen_shake_duration
    flash_timer = flash_duration

def update_effects(delta_time):
    global screen_shake_timer, flash_timer
    if screen_shake_timer > 0:
        screen_shake_timer -= delta_time
    if flash_timer > 0:
        flash_timer -= delta_time

def apply_screen_shake():
    if screen_shake_timer > 0:
        shake_intensity = 0.5  # Adjust as needed
        random_offset_x = random.uniform(-shake_intensity, shake_intensity)
        random_offset_y = random.uniform(-shake_intensity, shake_intensity)
        glTranslatef(random_offset_x, random_offset_y, 0)

def render_flash_effect():
    if flash_timer > 0:
        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Set orthographic projection to cover the whole screen
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(-1, 1, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Set the color to red with the alpha based on flash_timer
        glColor4f(1.0, 0.0, 0.0, min(flash_timer / flash_duration, 1.0))

        # Draw a full-screen quad for the red flash effect
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(1, -1)
        glVertex2f(1, 1)
        glVertex2f(-1, 1)
        glEnd()

        # Restore matrices and disable blending
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_BLEND)

# Main game loop
while True:
    # Get delta_time at the start of the loop
    delta_time = clock.tick(60) / 1000.0  # Limits to 60 FPS and gets time since last tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Handle keyboard events for movement without Shift
    if not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
        # X-Axis Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.x -= move_speed * delta_time
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.x += move_speed * delta_time

        # Y-Axis Movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.y += move_speed * delta_time
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.y -= move_speed * delta_time

    # *** Begin Z-Axis Movement ***
    # Handle Z-axis movement only when Shift is pressed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        # Z-Axis Movement with W/S (Forward/Backward)
        if keys[pygame.K_w]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.z += z_move_speed * delta_time  # Move forward along Z-axis
                        print(f"Shift + W: Moving cube to z={cube.z:.2f}")  # Debug statement
        if keys[pygame.K_s]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.z -= z_move_speed * delta_time  # Move backward along Z-axis
                        print(f"Shift + S: Moving cube to z={cube.z:.2f}")  # Debug statement

        # Z-Axis Movement with A/D (Left/Right)
        if keys[pygame.K_a]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.z -= z_move_speed * delta_time  # Move left along Z-axis
                        print(f"Shift + A: Moving cube to z={cube.z:.2f}")  # Debug statement
        if keys[pygame.K_d]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.z += z_move_speed * delta_time  # Move right along Z-axis
                        print(f"Shift + D: Moving cube to z={cube.z:.2f}")  # Debug statement

        # Z-Axis Movement with Left/Right Arrow Keys
        if keys[pygame.K_LEFT]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.z += z_move_speed * delta_time  # Move forward along Z-axis
                        print(f"Shift + Left Arrow: Moving cube to z={cube.z:.2f}")  # Debug statement
        if keys[pygame.K_RIGHT]:
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        cube.z -= z_move_speed * delta_time  # Move backward along Z-axis
                        print(f"Shift + Right Arrow: Moving cube to z={cube.z:.2f}")  # Debug statement
    # *** End Z-Axis Movement ***

    # *** Begin Portal and Grid Collision Detection ***
    if not is_animating:
        collision_detected = False
        for row in cubes:
            for layer in row:
                for cube in layer:
                    if not cube.is_destroyed:
                        if check_collision_with_horizon(cube) or check_collision_with_portal(cube):
                            collision_detected = True
                            break
                if collision_detected:
                    break
            if collision_detected:
                break

        if collision_detected:
            # Trigger collision response
            is_animating = True
            animation_timer = animation_duration
            print("Collision detected! Triggering cube destruction and animation.")

            # Set velocities for all small cubes to fly away
            for row in cubes:
                for layer in row:
                    for cube in layer:
                        if not cube.is_destroyed:
                            cube.destroy()

            # Trigger screen shake and flash effects
            trigger_hit_effects()
    # *** End Portal and Grid Collision Detection ***

    # *** Begin Animation Handling ***
    if is_animating:
        # Decrease the animation timer
        animation_timer -= delta_time

        # Calculate scaling factor (zoom effect)
        # Zoom in for the first half, then zoom out
        if animation_timer > animation_duration / 2:
            # Zoom in
            progress = (animation_duration - animation_timer) / (animation_duration / 2)
            animation_scale = 1.0 + progress  # Scale from 1.0 to 2.0
        else:
            # Zoom out
            progress = animation_timer / (animation_duration / 2)
            animation_scale = 1.0 + progress  # Scale from 2.0 back to 1.0

        # Draw the scene with the current scale
        draw_scene(animation_scale)
        pygame.display.flip()

        if animation_timer <= 0:
            is_animating = False
            animation_scale = 1.0
            print("Animation completed. Returning to the field.")
            # Optionally, reset cubes or perform other actions here
            reset_cubes(cubes)
        
        continue  # Skip the rest of the loop during animation
    # *** End Animation Handling ***

    # *** Begin Normal Rendering ***
    # Update effects
    update_effects(delta_time)

    # Update cube positions and flash status
    update_cubes(delta_time)

    # Check if all cubes are destroyed
    if all_cubes_destroyed(cubes):
        flash_screen()  # Flash the screen
        reset_cubes(cubes)  # Reset the cubes to start over
        continue  # Skip the rest of the loop to start with a fresh screen

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Apply screen shake
    glPushMatrix()  # Save the current state of transformations
    if screen_shake_timer > 0:
        apply_screen_shake()

    draw_scene(animation_scale=1.0)

    # Restore the original state after shake
    glPopMatrix()

    # Render the flash effect over the scene if needed
    if flash_timer > 0:
        render_flash_effect()

    # Update sway angles
    angle_x += rotation_speed * delta_time
    angle_y += rotation_speed * delta_time
    angle_z += rotation_speed * delta_time

    pygame.display.flip()
    # *** End Normal Rendering ***
