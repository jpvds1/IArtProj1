import pygame
from board import *
from pieces import *
from handlers import *

# Initialize Pygame
pygame.init()

# Game loop
running = True
turn = 0

# only for development
stack.init_pieces()

while running:
    screen.fill(BG_COLOR)
    draw_graph()
    stack.draw_stack_and_pieces(screen, turn)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Detect key press
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
            x, y = pygame.mouse.get_pos()
            turn = handle_click(x, y, turn)
        
    pygame.display.flip()

pygame.quit()
