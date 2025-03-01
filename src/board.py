import pygame
import math

# Screen settings
WIDTH, HEIGHT = 800, 800
SIZE = 5 # Size of the board
BG_COLOR = (255, 255, 255) # Background Color
NEUTRAL, WHITE, BLUE = 0, 1, 2 # Types of cells
COLORS = [(255, 255, 0), (255, 255, 255), (173, 216, 230)] # Colors of the cells
DIRECTIONS = ["UP", "UP_RIGHT", "DOWN_RIGHT", "DOWN", "DOWN_LEFT", "UP_LEFT"] # Possible directions of movement

# Screen with title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yonmoque Hex")

# Class that represents each cell in the board
class Cell:
    def __init__(self, id):
        self.id = id
        self.type = None # Type of cell (neutral, white, blue)
        self.piece = None  # None means empty cell
        self.neighbors = {dir: None for dir in DIRECTIONS} # None means no neighbor

    def set_neighbor(self, direction, node):
        self.neighbors[direction] = node


# Create a graph (list) with all the cells
def create_graph(size=5):
    # Create all the default cells
    cells = [Cell(i) for i in range(size * size)]

    # Set the neighbors for each cell
    for i in range(size * size):
        cell = cells[i]
        cell.type = WHITE
        
        if i % size != 0:  # Not first column
            cells[i - 1]. set_neighbor("DOWN_RIGHT", cell)
            cell.set_neighbor("UP_LEFT", cells[i - 1])

        if i >= size:  # Not first row
            cells[i - size].set_neighbor("DOWN_LEFT", cell)
            cell.set_neighbor("UP_RIGHT", cells[i - size])

        if i >= size + 1 and (i % size) != 0:  # Not first column and not first row
            cells[i - size - 1].set_neighbor("DOWN", cell)
            cell.set_neighbor("UP", cells[i - size - 1])
        
    # Set the blue cells    
    for i in range(size):
        cells[i].type = BLUE
        cells[size * size - i - 1].type = BLUE
        cells[i * size - 1].type = BLUE
        cells[i * size].type = BLUE
        
    # Set the neutral cells
    cells[0].type = NEUTRAL
    cells[size - 1].type = NEUTRAL
    cells[size * size - size].type = NEUTRAL
    cells[size * size - 1].type = NEUTRAL
    cells[size * size // 2].type = NEUTRAL

    return cells
            
graph = create_graph(SIZE)


# Draws an hexagon
def draw_hexagon(x, y, color, hex_radius, hex_id):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        px = x + hex_radius * math.cos(angle)
        py = y + hex_radius * math.sin(angle)
        points.append((px, py))
    
    # Draw an hexagon with a black outline
    pygame.draw.polygon(screen, color, points, 0)
    pygame.draw.polygon(screen, (0, 0, 0), points, 2)
    
    # Draw the id in the center (only for development purposes)
    font = pygame.font.Font(None, 24)
    text_surface = font.render(str(hex_id), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    
    screen.blit(text_surface, text_rect)


# Draw the board
def draw_graph():
    hex_radius = (WIDTH - 200) // (SIZE + (SIZE - 1 // 2)) / 2
    row_pos = [400, 200]
    
    for i in range(SIZE):
        col_pos = row_pos.copy()
        for d in range(SIZE):
            draw_hexagon(col_pos[0], col_pos[1], COLORS[graph[i * SIZE + d].type], hex_radius, graph[i * SIZE + d].id)
            col_pos[0] += hex_radius * 1.5
            col_pos[1] += hex_radius * math.sqrt(3) / 2
        row_pos[0] -= hex_radius * 1.5
        row_pos[1] += hex_radius * math.sqrt(3) / 2
