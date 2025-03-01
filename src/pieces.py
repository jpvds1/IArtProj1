import pygame
import math
from board import *

COLORS = [(255, 0, 0), (0, 255, 0)]
PIECES = []

class Piece:
    def __init__(self, player):
        self.player = player
        self.cell = None  # The Cell object this piece belongs to
        self.highlighted = False # Flag to check if the piece was selected

    def move_to(self, new_cell):
        if new_cell.piece is None:  # Check if the cell is empty
            self.cell.piece = None  # Remove from the current cell
            new_cell.piece = self  # Place in the new cell
            self.cell = new_cell  # Update the piece's position
        else:
            print("Invalid move! Cell is already occupied.")

    def draw(self, screen):
        if self.cell:
            x, y = self.cell.pos  # Get the cell's pixel position
            pygame.draw.circle(screen, COLORS[self.player], (x, y), HEX_RADIUS * 2 // 3)  # Draw piece
            if self.highlighted:
                pygame.draw.circle(screen, (100, 100, 100), (x, y), HEX_RADIUS * 2 // 3, 3)  # Draw highlighted outline
            else:
                pygame.draw.circle(screen, (0, 0, 0), (x, y), HEX_RADIUS * 2 // 3, 3)  # Draw outline
            
            return True
        return False
                
    def insert_piece(self, cell):
        if cell.piece is None:
            cell.piece = self
            self.cell = cell
        else:
            print("Cell already occupied.")

def draw_available(screen, available, player):
    x = 250 + 300 * player
    y = 600
    pygame.draw.circle(screen, COLORS[player], (x, y), HEX_RADIUS * 2 // 3)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), HEX_RADIUS * 2 // 3, 3)
    
    # Draw the id in the center (only for development purposes)
    font = pygame.font.Font(None, 24)
    text_surface = font.render("x" + str(available), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(x, y))
    
    screen.blit(text_surface, text_rect)

def draw_pieces(screen):
    available_pieces = [6, 6]
    for piece in PIECES:
        if piece.draw(screen):
            available_pieces[piece.player] -= 1
            
    draw_available(screen, available_pieces[0], 0)
    draw_available(screen, available_pieces[1], 1)
            
    
            
    

for i in range(6):
    piece = Piece(0)
    PIECES.append(piece)
    piece = Piece(1)
    PIECES.append(piece)


PIECES[2].insert_piece(graph[16])
PIECES[7].insert_piece(graph[6])