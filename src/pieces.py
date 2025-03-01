import pygame
import math
from board import *

COLORS = [(255, 0, 0), (0, 255, 0)]
PIECES = []

class Piece:
    def __init__(self, player):
        self.player = player
        self.cell = None  # The Cell object this piece belongs to

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
            pygame.draw.circle(screen, COLORS[self.player], (x, y), 20)  # Draw piece
            
    def insert_piece(self, cell):
        if cell.piece is None:
            cell.piece = self
            self.cell = cell
        else:
            print("Cell already occupied.")

def draw_pieces(screen):
    for piece in PIECES:
        piece.draw(screen)


piece = Piece(0)
piece.insert_piece(graph[3])
PIECES.append(piece)
piece = Piece(1)
piece.insert_piece(graph[6])
PIECES.append(piece)