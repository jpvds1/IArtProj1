from pieces import *
from board import *
import math
from enum import Enum

# This variable will be used to hold the selected piece when moving
PENDING_PIECE = None

# Enum with possible states
class States(Enum):
    DEFAULT = 0
    PENDING_MOVE = 1
    PENDING_PLACE = 2

STATE = States.DEFAULT

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

# Validate the move made (WIP)
def validate_move():
    return True

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
    global PENDING_PIECE, STATE
    
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
        elif piece == None and STATE == States.PENDING_MOVE:
            if validate_move():
                PENDING_PIECE.move_to(selected)
                PENDING_PIECE.highlighted = False
                PENDING_PIECE = None
                STATE = States.DEFAULT
                turn = 1 - turn
        elif piece == None and STATE == States.PENDING_PLACE:
            stack.place_piece(selected, turn)
            stack.highlighted = False
            STATE = States.DEFAULT
            turn = 1 - turn
        
    return turn
    
    
