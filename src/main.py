import pygame
from board import *

# Initialize Pygame
pygame.init()

# Game loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_graph()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    pygame.display.flip()

pygame.quit()
