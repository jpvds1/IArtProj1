import pygame
from board import *
from pieces import *
from handlers import *
from menu import *
import algorithm as alg


# Initialize Pygame
pygame.init()

def game_loop():
    start_game = main_menu()

    # Quit game
    if not start_game:
        pygame.quit()
        quit()

    # Determine game mode and bot configs
    if start_game[0] == "human_vs_computer":
        bot_configs = [start_game[1]]
    elif start_game[0] == "computer_vs_computer":
        bot_configs = [start_game[1], start_game[2]]
    else:
        bot_configs = []

    game_mode = start_game[0]
    running = True
    turn = 0
    winner = None
    setup_game()
    global graph
    graph = create_graph(SIZE)
    reset_handlers(graph)
    stack.__init__()

    # Development: add initial test pieces
    stack.init_pieces()

    while running:
        screen.fill(BG_COLOR)
        draw_graph()
        stack.draw_stack_and_pieces(screen, turn)

        # Human Player
        if game_mode == "human_vs_human" or (game_mode == "human_vs_computer" and turn == 0):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    result = handle_click(x, y, turn)
                    if isinstance(result, tuple):
                        turn, move_cell = result
                        if turn >= 2:
                            winner = turn - 2
                            choice = show_final_state(winner, move_cell, turn, stack)
                            if choice == "restart":
                                return True
                            running = False
                            break
                    else:
                        turn = result

        # AI logic
        else:
            algorithm_name, difficulty = bot_configs[turn if game_mode == "computer_vs_computer" else 0]
            pygame.display.flip()
            pygame.time.wait(1000)

            current_state = alg.GameState(graph, stack.pieces, stack)
            
            if algorithm_name == "MonteCarlo":
                iterations_map = {"Easy": 25, "Medium": 50, "Hard": 100}
                difficulty_str = "Easy Medium Hard".split()[difficulty - 1]
                iterations = iterations_map[difficulty_str]
                move = alg.best_move_mcts(current_state, turn, iterations)
            else:
                depth_map = {"Easy": 1, "Medium": 2, "Hard": 3}
                difficulty_str = "Easy Medium Hard".split()[difficulty - 1]
                depth = depth_map[difficulty_str]
                move = alg.best_move(current_state, turn, depth)

            if move[0] == "placement":
                selected_cell = next(c for c in graph if c.id == move[1].id)
                stack.place_piece(selected_cell, turn)
                move_cell = selected_cell
            elif move[0] == "move":
                origin = next(c for c in graph if c.id == move[1].id)
                destination = next(c for c in graph if c.id == move[2].id)
                if origin.piece:
                    origin.piece.move_to(destination)
                    check_flip(destination)
                    move_cell = destination

                if check_conditions(move_cell):
                    winner = turn
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    choice = show_final_state(winner, move_cell, turn, stack)
                    if choice == "restart":
                        return True
                    running = False
                    break

            pygame.time.wait(1000)
            turn = 1 - turn

        if turn >= 2:
            winner = turn - 1
            break

        pygame.display.flip()

    return False


# End screen after game over
while True:
    if not game_loop():
        break

pygame.quit()