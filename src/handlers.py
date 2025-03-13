from pieces import *
from board import *
import math
from enum import Enum
from typing import List

# This variable will be used to hold the selected piece when moving
PENDING_PIECE = None
VALID_MOVES = None
FIRST_MOVE = None

# Enum with possible states
class States(Enum):
    DEFAULT = 0
    PENDING_MOVE = 1
    PENDING_PLACE = 2

STATE = States.DEFAULT

# Setup variables before starting a game
def setup_game():
    global FIRST_MOVE
    FIRST_MOVE = True
    
# Check how many cells are in a row
def check_row(dir1, dir2, cell: Cell):
    cells_in_a_row = 1
    next_cell : Cell = cell.neighbors[dir1]
    while next_cell != None and next_cell.has_piece() and next_cell.piece.player == cell.piece.player:
        next_cell = next_cell.neighbors[dir1]
        cells_in_a_row += 1
    next_cell = cell.neighbors[dir2]
    while next_cell != None and next_cell.has_piece() and next_cell.piece.player == cell.piece.player:
        next_cell = next_cell.neighbors[dir2]
        cells_in_a_row += 1
    
    return cells_in_a_row


# Check if a win / loss condition has been met
# 0 : nothing
# 1 : win
# 2 : loss
def check_conditions(cell: Cell):
    cells_in_a_row = 1
    
    cells_in_a_row = max(cells_in_a_row, check_row("UP", "DOWN", cell))
    cells_in_a_row = max(cells_in_a_row, check_row("UP_RIGHT", "DOWN_LEFT", cell))
    cells_in_a_row = max(cells_in_a_row, check_row("UP_LEFT", "DOWN_RIGHT", cell))
        
    if cells_in_a_row > 4:
        return 2
    elif cells_in_a_row == 4:
        return 1
    else:
        return 0
        

# Check if a flip occurs after a move
def check_flip(cell: Cell):
    possible_flips = []
    current_cell = cell
    for direction in DIRECTIONS:
        next_cell : Cell = current_cell.neighbors[direction]
        while next_cell != None and next_cell.has_piece() and next_cell.piece.player != cell.piece.player:
            current_cell = next_cell
            next_cell : Cell = current_cell.neighbors[direction]
            possible_flips.append(current_cell.piece)
        if next_cell != None and next_cell.has_piece() and current_cell.neighbors[direction].piece.player == cell.piece.player:
            for piece in possible_flips:
                piece.flip()
        possible_flips.clear()
        current_cell = cell
        

# Recursive function, adds valid cells in a single direction until a move in impossible
# (color_switched) if the sequence of cells has already changed color
def validate_direction(direction, current_cell: Cell, piece: Piece, color_switched):
    possible_moves = []
    next_cell: Cell = current_cell.neighbors[direction]

    if next_cell == None:
        return possible_moves
    
    if next_cell.piece != None:
        return possible_moves
        
    # See if the color of the cell is equal to the color of the player
    cell_player_color = (piece.player == 0 and next_cell.type == BLUE) or (piece.player == 1 and next_cell.type == WHITE)

        
    if current_cell.type == next_cell.type:
        possible_moves.append(next_cell)
        if cell_player_color:
            possible_moves.extend(validate_direction(direction, next_cell, piece, color_switched))   
    elif color_switched == False:
        possible_moves.append(next_cell)
        if cell_player_color:    
            possible_moves.extend(validate_direction(direction, next_cell, piece, True))
            
            
    return possible_moves

# Fill a list of possible moves and highlight the possible cells
def valid_moves(piece: Piece):
    global VALID_MOVES
    VALID_MOVES = []
    current_cell = piece.cell
    for direction in DIRECTIONS:
        VALID_MOVES.extend(validate_direction(direction, current_cell, piece, False))
        
    for cell in VALID_MOVES:
        cell.highlighted = True
        

# Change the necessary values to setup a move
def setup_move(piece):
    global PENDING_PIECE, STATE
    piece.highlighted = True
    PENDING_PIECE = piece
    STATE = States.PENDING_MOVE
    return

# Change the necessary value to setup placing a piece
def setup_place():
    global STATE
    stack.highlighted = True
    STATE = States.PENDING_PLACE

# Move the piece and reset values
def make_move(cell: Cell):
    global PENDING_PIECE, STATE, VALID_MOVES
    PENDING_PIECE.move_to(cell)
    PENDING_PIECE.highlighted = False
    PENDING_PIECE = None
    for cell in VALID_MOVES:
        cell.highlighted = False
    STATE = States.DEFAULT


# Get the selected object
# Returns 0 or 1 when the stack of a player is selected
# Returns the cell when a cell is selected
# Returns None when nothing was selected
def get_selected(x, y):
    
    if math.sqrt((x - 250) ** 2 + (y - 600) ** 2) < HEX_RADIUS * 2 // 3:
        return 0
    
    if math.sqrt((x - 550) ** 2 + (y - 600) ** 2) < HEX_RADIUS * 2 // 3:
        return 1
    
    for cell in graph:
        cx, cy = cell.pos
        distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance < HEX_RADIUS:
            return cell
        
    return None

# Handle what happens when a click occurs
def handle_click(x, y, turn):
    global PENDING_PIECE, STATE, VALID_MOVES, FIRST_MOVE
    
    selected = get_selected(x, y)
    
    if selected is None:
        print("Nothing")
    
    elif selected == 0:
        if turn == 0 and STATE == States.DEFAULT:
            setup_place()
        
    elif selected == 1:
        if turn == 1 and STATE == States.DEFAULT:
            setup_place()
        
    else:
        piece = selected.piece
        if piece != None and STATE == States.DEFAULT and piece.player == turn:
            setup_move(piece)
            valid_moves(piece)
        elif piece == None and STATE == States.PENDING_MOVE:
            if selected in VALID_MOVES:
                make_move(selected)
                check_flip(selected)
                condition = check_conditions(selected)
                print(condition)
                turn = 1 - turn
            else:
                print("invalid move")
        elif piece == None and STATE == States.PENDING_PLACE:
            is_corner = selected.id == 0 or selected.id == SIZE - 1 or selected.id == SIZE * SIZE - SIZE or selected.id == SIZE * SIZE - 1
            if not (FIRST_MOVE and is_corner):
                FIRST_MOVE = False
                stack.place_piece(selected, turn)
                stack.highlighted = False
                STATE = States.DEFAULT
                turn = 1 - turn
        
    return turn