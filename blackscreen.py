"""
Shows a black screen in between two images.
"""

import pygame


def show_black_screen(screen, duration):
    screen.fill((0, 0, 0))  # Fill with black color
    pygame.display.flip()  # Flip the screen to display the black screen
    pygame.time.wait(int(duration))  # Wait in milliseconds
