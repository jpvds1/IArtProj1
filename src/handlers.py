from pieces import *
from board import *
import math

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

def handle_click(x, y):
    selected = get_selected(x, y)
    
    if selected is None:
        print("Nothing")
    
    elif selected == 0:
        print("player 0")
        
    elif selected == 1:
        print("player 1")
        
    else:
        print(selected.id)
    
    
