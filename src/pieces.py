import pygame
import math
from board import *

COLORS = [(255, 0, 0), (0, 255, 0)]

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

class Stack:
    def __init__(self):
        self.stack = [6, 6]
        self.pieces = []
        
    def remove(self, player):
        if self.stack[player] > 0:
            self.stack[player] -= 1
                
    def draw_available(self, screen, player):
        x = 250 + 300 * player
        y = 600
        
        pygame.draw.circle(screen, COLORS[player], (x, y), HEX_RADIUS * 2 // 3)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), HEX_RADIUS * 2 // 3, 3)
        
        # Write the number of pieces left
        font = pygame.font.Font(None, 24)
        text_surface = font.render("x" + str(self.stack[player]), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        
        screen.blit(text_surface, text_rect)

    def draw_stack(self, screen):
        self.draw_available(screen, 0)
        self.draw_available(screen, 1)
        
    # only for development
    def init_pieces(self):
        piece = Piece(0)
        self.pieces.append(piece)
        piece = Piece(1)
        self.pieces.append(piece)
            
        self.pieces[0].insert_piece(graph[16])
        self.pieces[1].insert_piece(graph[6])
        
    def draw_stack_and_pieces(self, screen):
        for piece in self.pieces:
            piece.draw(screen)
        self.draw_stack(screen)
            
stack = Stack()