import pygame

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Polygon Drawing")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    window.fill((0, 0, 0))

    # Draw a polygon
    pygame.draw.polygon(window, (255, 255, 255), [(100, 100), (200, 50), (300, 100), (250, 200)])

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
