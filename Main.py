import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
SIZE = 5
BG_COLOR = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
PLAYER_COLORS = [(255, 100, 100), (100, 100, 255)]
DIRECTIONS = ["UP", "UP_RIGHT", "DOWN_RIGHT", "DOWN", "DOWN_LEFT", "UP_LEFT"]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yonmoque Hex")

# Class that represents each cell in the board
class Cell:
    def __init__(self, id):
        self.id = id
        self.color = GRID_COLOR
        self.piece = None  # None means empty cell
        self.neighbors = {dir: None for dir in DIRECTIONS} # None means no neighbor

    def set_neighbor(self, direction, node):
        self.neighbors[direction] = node


def create_graph(size=5):
    cells = [Cell(i) for i in range(size * size)]

    for i in range(size * size):
        cell = cells[i]

        if i % size != 0:  # Not first column
            cells[i - 1].neighbors["DOWN_RIGHT"] = cell
            cell.neighbors["UP_LEFT"] = cells[i - 1]

        if i >= size:  # Not first row
            cells[i - size].neighbors["DOWN_LEFT"] = cell
            cell.neighbors["UP_RIGHT"] = cells[i - size]

        if i >= size + 1 and (i % size) != 0:  # Not first column and not first row
            cells[i - size - 1].neighbors["DOWN"] = cell
            cell.neighbors["UP"] = cells[i - size - 1]

    return cells
            
graph = create_graph(SIZE)

def draw_hexagon(x, y, color, hex_radius, hex_id):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        px = x + hex_radius * math.cos(angle)
        py = y + hex_radius * math.sin(angle)
        points.append((px, py))
    
    pygame.draw.polygon(screen, color, points, 2)
    
    # Render text in the center
    font = pygame.font.Font(None, 24)  # Default font, size 24
    text_surface = font.render(str(hex_id), True, (255, 255, 255))  # White text
    text_rect = text_surface.get_rect(center=(x, y))
    
    screen.blit(text_surface, text_rect)


def draw_graph():
    
    hex_radius = (WIDTH - 200) // (SIZE + (SIZE - 1 // 2)) / 2
    center_hex = SIZE * SIZE // 2 + 1
    
    row_size = 1
    current_id = 0
    
    row_pos = [400, 200]
    
    for i in range(SIZE):
        col_pos = row_pos.copy()
        for d in range(SIZE):
            draw_hexagon(col_pos[0], col_pos[1], (255, 0, 0), hex_radius, graph[i * SIZE + d].id)
            col_pos[0] += hex_radius * 1.5
            col_pos[1] += hex_radius * math.sqrt(3) / 2
        row_pos[0] -= hex_radius * 1.5
        row_pos[1] += hex_radius * math.sqrt(3) / 2
            
        
    
    return

draw_graph()

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
