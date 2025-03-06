import pygame

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
BG_COLOR = (255, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (173, 216, 230)
BUTTON_HOVER_COLOR = (0, 0, 255)
FONT = pygame.font.Font(None, 35)
TITLE = pygame.font.Font(None, 50)


# Screen with title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yonmoque Hex")


# Draw buttons
def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        if click[0] == 1 and action:
            return action()
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))

    text_surf = FONT.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)


# Show the main menu
def main_menu():
    while True:
        screen.fill(BG_COLOR)
        
        title_text = TITLE.render("Welcome to Yonmoque-Hex!", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        if draw_button("Human vs. Human", WIDTH // 2 - 150, 250, 300, 50, start_game):
            return True
        if draw_button("Human vs. Computer", WIDTH // 2 - 150, 320, 300, 50, not_implemented):
            return "human_vs_computer"
        if draw_button("Computer vs. Computer", WIDTH // 2 - 150, 390, 300, 50, not_implemented):
            return "computer_vs_computer"
        if draw_button("Rules", WIDTH // 2 - 150, 490, 300, 50, show_rules):
            pass
        if draw_button("Quit", WIDTH // 2 - 150, 560, 300, 50, quit_game):
            return False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


# Starting the game (currently only Human vs. Human working)
def start_game():
    return True


# Show rules (sub-menu)
def show_rules():
    rules_text = [
        "Yonmoque-Hex is a game.",
        "Press ESC to return to the main menu."
    ]

    running = True
    while running:
        screen.fill(BG_COLOR)
        title_text = TITLE.render("Game Rules", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        # Display each rule
        for i, rule in enumerate(rules_text):
            rule_text = FONT.render(rule, True, BLACK)
            screen.blit(rule_text, (WIDTH // 2 - rule_text.get_width() // 2, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to return
                    running = False


# Function to quit the game
def quit_game():
    pygame.quit()
    quit()


# Only while not all modes are implemented
def not_implemented():
    print("This mode is not implemented yet!")