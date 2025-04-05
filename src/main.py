import pygame
from board import *
from pieces import *
from handlers import *
from menu import *
from algorithm import *

# Initialize Pygame
pygame.init()

start_game = main_menu()

# Quit game
if not start_game:
    pygame.quit()
    quit()

game_mode = start_game[0]

if game_mode == "human_vs_computer":
    bot_configs = [start_game[1]]  # uma config só
elif game_mode == "computer_vs_computer":
    bot_configs = [start_game[1], start_game[2]]  # duas configs
else:
    bot_configs = []


# Game loop
running = True
turn = 0
winner = None
setup_game()

# only for development
stack.init_pieces()

if isinstance(start_game, tuple):
    game_mode = start_game[0]
    bot_configs = start_game[1:]

while running:
    screen.fill(BG_COLOR)
    draw_graph()
    stack.draw_stack_and_pieces(screen, turn)

    if game_mode == "human_vs_human" or (game_mode == "human_vs_computer" and turn == 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                turn = handle_click(x, y, turn)

    else:
        # Turno do computador
        algorithm, level = bot_configs[turn if game_mode == "computer_vs_computer" else 0]
        depth = {"Easy": 1, "Medium": 2, "Hard": 3}[["Easy", "Medium", "Hard"][level - 1]]

        pygame.display.flip() 
        pygame.time.wait(1000)

        best_move = get_best_move(stack.pieces, stack, turn, depth)
        affected_piece, flips_made = apply_move(best_move, turn, stack.pieces, stack)
        outcome = immediate_check_win(affected_piece.cell)

        if outcome == "WIN":
            winner = turn
            break
        elif outcome == "LOSS":
            winner = 1 - turn
            break

        turn = 1 - turn

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
