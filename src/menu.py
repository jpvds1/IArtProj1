import pygame
from board import *

pygame.init()

# Basic display settings
WIDTH, HEIGHT = 800, 800
BG_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (173, 216, 230)
BUTTON_HOVER_COLOR = (0, 0, 255)
FONT = pygame.font.Font(None, 35)
TITLE = pygame.font.Font(None, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yonmoque Hex")

# Draw a clickable button
def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        if click[0] == 1:
            pygame.time.wait(150)
            if action:
                return action()
            return True
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))

    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Menu for configuring bot for Human vs. Computer mode
def bot_config_menu(player_name):
    pygame.event.clear()
    levels = ['Easy', 'Medium', 'Hard']
    selected_algorithm = "Minimax"
    selected_level = 2

    while True:
        screen.fill(BG_COLOR)

        title_text = TITLE.render(f"{player_name} Bot Configuration", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        if draw_button(f"Algorithm: {selected_algorithm}", WIDTH // 2 - 150, 180, 300, 50):
            selected_algorithm = "MonteCarlo" if selected_algorithm == "Minimax" else "Minimax"
            pygame.time.wait(100)

        if draw_button(f"Difficulty: {levels[selected_level]}", WIDTH // 2 - 150, 250, 300, 50):
            selected_level = (selected_level + 1) % len(levels)

        if draw_button("Confirm", WIDTH // 2 - 150, 390, 300, 50):
            return selected_algorithm, selected_level + 1

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Menu for configuring both bots in Computer vs. Computer mode
def cc_config_menu():
    pygame.event.clear()
    levels = ['Easy', 'Medium', 'Hard']
    selected_level1 = 2
    selected_level2 = 2
    selected_algorithm1 = "Minimax"
    selected_algorithm2 = "Minimax"

    while True:
        screen.fill(BG_COLOR)

        title = TITLE.render("Computer vs. Computer", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        comp1_text = FONT.render("Computer 1", True, BLACK)
        screen.blit(comp1_text, (WIDTH // 4 - comp1_text.get_width() // 2, 120))

        if draw_button(f"Algorithm: {selected_algorithm1}", WIDTH // 4 - 150, 170, 300, 50):
            selected_algorithm1 = "MonteCarlo" if selected_algorithm1 == "Minimax" else "Minimax"
            pygame.time.wait(100)

        if draw_button(f"Difficulty: {levels[selected_level1]}", WIDTH // 4 - 150, 240, 300, 50):
            selected_level1 = (selected_level1 + 1) % len(levels)

        comp2_text = FONT.render("Computer 2", True, BLACK)
        screen.blit(comp2_text, (3 * WIDTH // 4 - comp2_text.get_width() // 2, 120))

        if draw_button(f"Algorithm: {selected_algorithm2}", 3 * WIDTH // 4 - 150, 170, 300, 50):
            selected_algorithm2 = "MonteCarlo" if selected_algorithm2 == "Minimax" else "Minimax"
            pygame.time.wait(100)

        if draw_button(f"Difficulty: {levels[selected_level2]}", 3 * WIDTH // 4 - 150, 240, 300, 50):
            selected_level2 = (selected_level2 + 1) % len(levels)

        if draw_button("Confirm", WIDTH // 2 - 150, 320, 300, 50):
            return (selected_algorithm1, selected_level1 + 1), (selected_algorithm2, selected_level2 + 1)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Show the main menu and return selected game mode
def main_menu():
    while True:
        screen.fill(BG_COLOR)

        title = TITLE.render("Welcome to Yonmoque-Hex!", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        if draw_button("Human vs. Human", WIDTH // 2 - 150, 250, 300, 50, start_game):
            return ("human_vs_human",)
        if draw_button("Human vs. Computer", WIDTH // 2 - 150, 320, 300, 50):
            return ("human_vs_computer", bot_config_menu("Computer"))
        if draw_button("Computer vs. Computer", WIDTH // 2 - 150, 390, 300, 50):
            configs = cc_config_menu()
            return ("computer_vs_computer",) + configs
        if draw_button("Rules", WIDTH // 2 - 150, 490, 300, 50, show_rules):
            pass
        if draw_button("Quit", WIDTH // 2 - 150, 560, 300, 50, quit_game):
            return False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Called when starting the game manually
def start_game():
    return True

# Show the game rules
def show_rules():
    rules = [
        "Yonmoque-Hex is a turn-based strategy game.",
        "Avoid making a 5-piece line.",
        "Make a 4-piece line to win.",
        "Press ESC to return to menu."
    ]
    running = True
    while running:
        screen.fill(BG_COLOR)
        title = TITLE.render("Game Rules", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for i, rule in enumerate(rules):
            rule_text = FONT.render(rule, True, BLACK)
            screen.blit(rule_text, (WIDTH // 2 - rule_text.get_width() // 2, 200 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# Show the final game state and winner
def show_final_state(winner, last_move, turn, stack):
    final_font = pygame.font.Font(None, 35)

    while True:
        screen.fill(BG_COLOR)
        draw_graph()
        stack.draw_stack_and_pieces(screen, turn)

        if last_move is not None:
            x, y = last_move.pos
            pygame.draw.circle(screen, (255, 255, 0), (x, y), HEX_RADIUS * 2 // 3 + 5, 3)

        message = f"Player {winner + 1} won!"
        text_surface = final_font.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 150))
        screen.blit(text_surface, text_rect)

        if draw_button("Play Again", WIDTH // 2 - 300 - 20 // 2, HEIGHT - 100, 300, 50):
            return "restart"
        if draw_button("Quit", WIDTH // 2 + 20 // 2, HEIGHT - 100, 300, 50):
            return "quit"

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"


# Function to quit the game
def quit_game():
    pygame.quit()
    quit()
