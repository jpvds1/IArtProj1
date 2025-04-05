from board import graph, DIRECTIONS, SIZE
from pieces import Piece, stack
from handlers import check_conditions
import random


WIN_SCORE = 10000
LOSS_SCORE = -10000
STRONG_THREAT = 500
WEAK_THREAT = 50
OPPONENT_THREAT = -300
SMALL_ADVANTAGE = 30
MINOR_ADVANTAGE = 10
MINOR_DISADVANTAGE = -20
SLIGHT_DISADVANTAGE = -5



# Recursively finds all valid cells a piece can move to in a specific direction
def validate_direction_static(direction, current_cell, piece, color_switched):
    possible_moves = []
    next_cell = current_cell.neighbors[direction]

    if next_cell is None or next_cell.piece is not None:
        return possible_moves

    # Check if the cell matches the player's color
    cell_matches_player = (
        (piece.player == 0 and next_cell.type == 2) or
        (piece.player == 1 and next_cell.type == 1)
    )

    if current_cell.type == next_cell.type:
        possible_moves.append(next_cell)
        if cell_matches_player:
            possible_moves.extend(validate_direction_static(direction, next_cell, piece, color_switched))
    elif not color_switched:
        possible_moves.append(next_cell)
        if cell_matches_player:
            possible_moves.extend(validate_direction_static(direction, next_cell, piece, True))

    return possible_moves


# Returns all valid destination cells for a specific piece
def get_valid_moves_for_piece(piece):
    current_cell = piece.cell
    all_moves = []
    for direction in DIRECTIONS:
        all_moves.extend(validate_direction_static(direction, current_cell, piece, False))
    return all_moves


# Returns all valid empty cells for new piece placement
def get_possible_placements(graph, pieces):
    occupied_ids = {piece.cell.id for piece in pieces if piece.cell}
    placements = [cell for cell in graph if cell.piece is None and cell.id not in occupied_ids]
    
    # Se nenhuma peça foi colocada, é a primeira jogada; elimina os cantos:
    if all(piece.cell is None for piece in pieces) or len([p for p in pieces if p.cell is not None]) == 0:
        prohibited = {0, SIZE - 1, SIZE * SIZE - SIZE, SIZE * SIZE - 1}
        placements = [cell for cell in placements if cell.id not in prohibited]
        
    return placements



# Returns all valid moves for a given player (placements and movements)
def get_possible_moves(pieces, player):
    moves = []

    # Piece movements
    for piece in pieces:
        if piece.player == player and piece.cell:
            for dest in get_valid_moves_for_piece(piece):
                moves.append((piece, dest))

    # New piece placement (if player has any left)
    if stack.stack[player] > 0:
        for cell in get_possible_placements(graph, pieces):
            moves.append(('place', cell))

    return moves


# Counts how many pieces in a line (both directions)
def count_in_line(cell, dir1, dir2, player):
    total = 1
    for direction in [dir1, dir2]:
        current = cell.neighbors.get(direction)
        while current and current.piece and current.piece.player == player:
            total += 1
            current = current.neighbors.get(direction)
    return total


# Basic heuristic to guess if a line was created via placement
def was_placement_sequence(cell, dir1, dir2):
    return cell.id in [0, SIZE - 1, SIZE * SIZE - SIZE, SIZE * SIZE - 1]


# Checks if a piece's move caused a win or loss
def check_win_for_piece(cell):
    if cell is None or cell.piece is None:
        return None  # Se não houver peça, não há condição de vitória
    def count(cell, dir1, dir2):
        total = 1
        for direction in [dir1, dir2]:
            next_cell = cell.neighbors.get(direction)
            while next_cell and next_cell.piece and next_cell.piece.player == cell.piece.player:
                total += 1
                next_cell = next_cell.neighbors.get(direction)
        return total

    for dir1, dir2 in [("UP", "DOWN"), ("UP_RIGHT", "DOWN_LEFT"), ("UP_LEFT", "DOWN_RIGHT")]:
        total = count(cell, dir1, dir2)
        if total > 4:
            return "LOSS"
        elif total == 4:
            return "WIN"
    return None




def apply_move(move, player, pieces, stack):
    flips_made = []

    if move[0] == 'place':
        dest_cell = move[1]
        new_piece = Piece(player)
        new_piece.insert_piece(dest_cell)
        pieces.append(new_piece)
        stack.stack[player] -= 1
        affected_piece = new_piece
    else:
        piece, dest_cell = move
        piece.move_to(dest_cell)
        affected_piece = piece
        flips_made = apply_flips(dest_cell, player)

    return affected_piece, flips_made


def undo_move(move, player, pieces, stack, affected_piece, flips_made):
    if move[0] == 'place':
        stack.stack[player] += 1
        # Limpar a célula onde a nova peça foi colocada
        affected_piece.cell.piece = None
        pieces.remove(affected_piece)
    else:
        # Para movimentos, restauramos manualmente o estado:
        # 1. Removemos a peça da célula de destino atual
        current_cell = affected_piece.cell
        current_cell.piece = None
        # 2. Recolocamos a peça na célula original (guardada em affected_piece.original_cell)
        original_cell = affected_piece.original_cell
        original_cell.piece = affected_piece
        affected_piece.cell = original_cell

        # Reverte os flips efetuados (que trocam o jogador da peça)
        for flipped_piece in flips_made:
            flipped_piece.flip()


def immediate_check_win(cell):
    result = check_win_for_piece(cell)
    return result

def apply_flips(cell, player):
    flips = []
    for direction in DIRECTIONS:
        current = cell
        potential_flips = []

        while True:
            neighbor = current.neighbors.get(direction)
            if neighbor is None or neighbor.piece is None:
                break
            if neighbor.piece.player == player:
                flips.extend(potential_flips)
                for p in potential_flips:
                    p.flip()
                break
            else:
                potential_flips.append(neighbor.piece)
                current = neighbor
    return flips


def heuristic(pieces, player):
    score = 0
    opponent = 1 - player
    for piece in pieces:
        if piece.cell is None:
            continue
        current_player = piece.player
        for dir1, dir2 in [("UP", "DOWN"), ("UP_RIGHT", "DOWN_LEFT"), ("UP_LEFT", "DOWN_RIGHT")]:
            count_line = count_in_line(piece.cell, dir1, dir2, current_player)
            # Se o adversário tiver 3 ou 4 em linha, aumenta a prioridade para bloqueá-los
            if current_player == opponent:
                if count_line == 3:
                    score += OPPONENT_THREAT * 1.5
                elif count_line == 4:
                    score += OPPONENT_THREAT * 2
            else:
                if count_line >= 5:
                    return LOSS_SCORE if current_player == player else WIN_SCORE
                elif count_line == 4:
                    score += WEAK_THREAT if was_placement_sequence(piece.cell, dir1, dir2) else STRONG_THREAT
                elif count_line == 3:
                    score += SMALL_ADVANTAGE if current_player == player else MINOR_DISADVANTAGE
                elif count_line == 2:
                    score += MINOR_ADVANTAGE if current_player == player else SLIGHT_DISADVANTAGE
    return score



def minimax(pieces, stack, depth, alpha, beta, maximizing, player):
    opponent = 1 - player
    if depth == 0:
        return heuristic(pieces, player)

    moves = get_possible_moves(pieces, player if maximizing else opponent)
    if not moves:
        return heuristic(pieces, player)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            snapshot = create_snapshot(pieces, stack)
            
            affected_piece, flips_made = apply_move(move, player, pieces, stack)
            outcome = immediate_check_win(affected_piece.cell)
            if outcome == "WIN":
                eval_value = WIN_SCORE
            elif outcome == "LOSS":
                eval_value = LOSS_SCORE
            else:
                eval_value = minimax(pieces, stack, depth - 1, alpha, beta, False, player)
            
            restore_snapshot(snapshot, pieces, stack)
            
            max_eval = max(max_eval, eval_value)
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            snapshot = create_snapshot(pieces, stack)
            
            affected_piece, flips_made = apply_move(move, opponent, pieces, stack)
            outcome = immediate_check_win(affected_piece.cell)
            if outcome == "WIN":
                eval_value = LOSS_SCORE
            elif outcome == "LOSS":
                eval_value = WIN_SCORE
            else:
                eval_value = minimax(pieces, stack, depth - 1, alpha, beta, True, player)
            
            restore_snapshot(snapshot, pieces, stack)
            
            min_eval = min(min_eval, eval_value)
            beta = min(beta, eval_value)
            if beta <= alpha:
                break
        return min_eval



def get_best_move(pieces, stack, player, depth=2):
    best_value = float('-inf')
    best_moves = []
    possible_moves = get_possible_moves(pieces, player)
    
    if not possible_moves:
        placements = get_possible_placements(graph, pieces)
        if placements:
            return ('place', placements[0])
        else:
            return None

    for move in possible_moves:
        snapshot = create_snapshot(pieces, stack)
        
        affected_piece, flips_made = apply_move(move, player, pieces, stack)
        outcome = immediate_check_win(affected_piece.cell)
        
        if outcome == "WIN":
            value = WIN_SCORE
        elif outcome == "LOSS":
            value = LOSS_SCORE
        else:
            value = minimax(pieces, stack, depth - 1, float('-inf'), float('inf'), False, player)
        
        restore_snapshot(snapshot, pieces, stack)
        
        if value > best_value:
            best_value = value
            best_moves = [move]
        elif value == best_value:
            best_moves.append(move)
    
    # Se houver mais de uma jogada com a melhor pontuação, escolhe aleatoriamente
    return random.choice(best_moves) if best_moves else None



import copy

def create_snapshot(pieces, stack):
    """
    Cria um snapshot do estado dinâmico do jogo.
    Para cada peça, guarda uma tupla com:
      (player, cell_id, original_cell_id, highlighted)
    """
    snapshot = {
        'pieces': [
            (
                piece.player,
                piece.cell.id if piece.cell is not None else None,
                piece.original_cell.id if piece.original_cell is not None else None,
                piece.highlighted
            ) for piece in pieces
        ],
        'stack': stack.stack.copy()
    }
    return snapshot

def restore_snapshot(snapshot, pieces, stack):
    """
    Restaura o estado dinâmico do jogo a partir do snapshot.
    Recria a lista de peças e atualiza as células do tabuleiro.
    """
    # Limpa a ocupação das células do tabuleiro
    for cell in graph:
        cell.piece = None

    # Limpa a lista atual de peças e recria a partir do snapshot
    pieces.clear()
    for (player, cell_id, original_cell_id, highlighted) in snapshot['pieces']:
        piece = Piece(player)
        piece.highlighted = highlighted
        if cell_id is not None:
            piece.cell = graph[cell_id]
            graph[cell_id].piece = piece
        else:
            piece.cell = None
        if original_cell_id is not None:
            piece.original_cell = graph[original_cell_id]
        else:
            piece.original_cell = None
        pieces.append(piece)

    # Restaura o estado da pilha
    stack.stack = snapshot['stack'].copy()




'''
def test_minimax_decision():
    from pieces import Piece, stack
    from board import graph

    # Limpar peças atuais
    stack.pieces.clear()
    stack.stack = [6, 6]  # Reset das peças disponíveis para cada jogador

    # Criar peças do jogador 0 (nas células 6, 11, 15, 21)
    for id in [6, 11, 15, 21]:
        piece = Piece(0)
        cell = graph[id]
        piece.insert_piece(cell)
        stack.pieces.append(piece)

    # Criar peças do jogador 1 (nas células 3, 13)
    for id in [3, 13]:
        piece = Piece(1)
        cell = graph[id]
        piece.insert_piece(cell)
        stack.pieces.append(piece)

    # Obter a melhor jogada para o jogador 0
    best_move = get_best_move(stack.pieces, stack, 0, depth=2)
    print("Melhor jogada para o jogador 0:", format_move(best_move))

def test_minimax_decision_player1():
    from pieces import Piece, stack
    from board import graph

    # Limpar peças atuais
    stack.pieces.clear()
    stack.stack = [6, 6]

    # Criar peças do jogador 0 (nas células 6, 11, 15, 21)
    for id in [6, 11, 15, 21]:
        piece = Piece(0)
        cell = graph[id]
        piece.insert_piece(cell)
        stack.pieces.append(piece)

    # Criar peças do jogador 1 (nas células 3, 13)
    for id in [3, 13]:
        piece = Piece(1)
        cell = graph[id]
        piece.insert_piece(cell)
        stack.pieces.append(piece)

    # Obter a melhor jogada para o jogador 1
    best_move = get_best_move(stack.pieces, stack, 1, depth=2)
    print("Melhor jogada para o jogador 1:", format_move(best_move))


def format_move(move):
    if move[0] == 'place':
        return f"Colocar peça na célula {move[1].id}"
    else:
        return f"Mover peça da célula {move[0].cell.id} para célula {move[1].id}"


if __name__ == "__main__":
    print("--- Jogador 0 ---")
    #test_minimax_decision()
    print("--- Jogador 1 ---")
    test_minimax_decision_player1()
'''

