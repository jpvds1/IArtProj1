import pygame
from board import *
from pieces import *
from handlers import *
from menu import *

# Initialize Pygame
pygame.init()

start_game = main_menu()

# Quit game
if not start_game:
    pygame.quit()
    quit()

# Game loop
running = True
turn = 0
winner = None
setup_game()

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
    
    if turn >= 2:
        winner = turn - 1
        break
    
    pygame.display.flip()

running = True
while running:
    end_game(winner)    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # Detect key press
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
