import pygame
import math


# Screen settings
WIDTH, HEIGHT = 800, 800
SIZE = 5 # Size of the board
HEX_RADIUS = (WIDTH - 200) // (SIZE + (SIZE - 1 // 2)) / 2
BG_COLOR = (255, 255, 255) # Background Color
NEUTRAL, WHITE, BLUE = 0, 1, 2 # Types of cells
COLORS = [(255, 255, 255), (255, 255, 255), (173, 216, 230)] # Colors of the cells
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
        self.pos = None
        self.highlighted = False
        self.neighbors : Cell = {dir: None for dir in DIRECTIONS} # None means no neighbor

    def set_neighbor(self, direction, node):
        self.neighbors[direction] = node
        
    def has_piece(self):
        return self.piece != None
    
    def has_neighbor(self, direction):
        return self.neighbors[direction] != None


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
    
    
    # Set the positions of the cells
    row_pos = [400, 200]
    
    for i in range(SIZE):
        col_pos = row_pos.copy()
        for d in range(SIZE):
            cells[i * size + d].pos = (col_pos[0], col_pos[1])
            col_pos[0] += HEX_RADIUS * 1.5
            col_pos[1] += HEX_RADIUS * math.sqrt(3) / 2
        row_pos[0] -= HEX_RADIUS * 1.5
        row_pos[1] += HEX_RADIUS * math.sqrt(3) / 2

    return cells
            
graph = create_graph(SIZE)


# Draws an hexagon
def draw_hexagon(x, y, type, HEX_RADIUS, highlighted):
    points = []
    for i in range(6):
        angle = math.pi / 3 * i
        px = x + HEX_RADIUS * math.cos(angle)
        py = y + HEX_RADIUS * math.sin(angle)
        points.append((px, py))
    
    # Draw an hexagon with a black outline
    pygame.draw.polygon(screen, COLORS[type], points, 0)
    if highlighted:
        pygame.draw.polygon(screen, (0, 255, 255), points, 2)
    else:
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)
    
    if type == NEUTRAL:
        font = pygame.font.Font(None, 24)
        text_surface = font.render("N", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))

        screen.blit(text_surface, text_rect)


# Draw the board (highlighted cells last)
def draw_graph():
    
    for cell in graph:
        if cell.highlighted == False:
            x, y = cell.pos
            draw_hexagon(x, y, cell.type, HEX_RADIUS, cell.highlighted)
            
    for cell in graph:
        if cell.highlighted == True:
            x, y = cell.pos
            draw_hexagon(x, y, cell.type, HEX_RADIUS, cell.highlighted)
