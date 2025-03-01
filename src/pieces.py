import pygame
import math

COLORS = [(255, 0, 0), (0, 255, 0)]

class Piece:
    def __init__(self, player, cell):
        self.player = player
        self.cell = cell  # The Cell object this piece belongs to

    def move_to(self, new_cell):
        if new_cell.piece is None:  # Check if the cell is empty
            self.cell.piece = None  # Remove from the current cell
            new_cell.piece = self  # Place in the new cell
            self.cell = new_cell  # Update the piece's position
        else:
            print("Invalid move! Cell is already occupied.")

    def draw(self, screen):
        """Draw the piece in the center of its hex cell."""
        if self.cell:
            x, y = self.cell.pixel_pos  # Get the cell's pixel position
            pygame.draw.circle(screen, COLORS[self.player], (x, y), 20)  # Draw piece
