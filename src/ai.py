import copy
import random
from pieces import Piece, Stack
from board import graph, DIRECTIONS
from algorithm import *


class Node:
    def __init__(self, state, player, parent=None):
        self.state = state  # Estado do tabuleiro (grafo)
        self.player = player  # Jogador atual
        self.parent = parent  # Nó pai
        self.children = []  # Filhos do nó
        self.visits = 0  # Número de visitas ao nó
        self.results = {0: 0, 1: 0}  # Resultados do nó
        self.availableMoves = self.getAvailableMoves()

    def getAvailableMoves(self):
        # Usa a função de movimentos possíveis de algorithm.py
        moves = get_possible_moves(self.state, self.player)
        return moves

    def isFullyExpanded(self):
        return len(self.availableMoves) == 0

    def getUCT(self):
        if self.visits == 0:
            return float('inf')
        win_rate = self.results[self.player] / self.visits
        exploration = (2 * (self.parent.visits ** 0.5)) / self.visits
        return win_rate + exploration


class MonteCarloTreeSearch:
    def __init__(self, explorationConstant=1.4):
        self.explorationConstant = explorationConstant

    def otherPlayer(self, player):
        return 1 - player

    def isTerminal(self, node):
        # Verifica vitória ou derrota usando as funções de algorithm.py
        return check_win_for_piece(node.state) is not None

    def search(self, initialState, player, maxIterations=100):
        root = Node(initialState, player)
        for _ in range(maxIterations):
            node = root
            state = copy.deepcopy(initialState)
            while not self.isTerminal(node):
                if not node.isFullyExpanded():
                    self.expand(node, state)
                else:
                    node = self.select(node)
            score = self.simulation(node, state)
            self.backpropagate(node, score)
        return self.getBestMove(root)

    def select(self, node):
        if not node.children:
            return node
        return max(node.children, key=lambda child: child.getUCT())

    def expand(self, node, state, max_depth=3):
        if len(node.availableMoves) == 0 or node.parent and node.parent.visits >= max_depth:
            return
        move = node.availableMoves.pop(0)
        newState = copy.deepcopy(state)
        # Recupera as posições equivalentes no novo estado
        from_cell = next(cell for cell in newState if cell.id == move[0].id)
        to_cell = next(cell for cell in newState if cell.id == move[1].id)
        from_cell.piece.move_to(to_cell)

        childNode = Node(newState, self.otherPlayer(node.player), node)
        node.children.append(childNode)

    def simulation(self, node, state, maxSimulations=50):
        simulations = 0
        while not self.isTerminal(node) and simulations < maxSimulations:
            moves = node.getAvailableMoves()
            if not moves:
                break
            move = random.choice(moves)
            from_cell = next(cell for cell in state if cell.id == move[0].id)
            to_cell = next(cell for cell in state if cell.id == move[1].id)
            from_cell.piece.move_to(to_cell)
            node = Node(state, self.otherPlayer(node.player), node)
            simulations += 1
        return node.parent.player if node.parent else 0

    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.results[score] += 1
            node = node.parent

    def getBestMove(self, node):
        if not node.children:
            return None, None
        return max(node.children, key=lambda child: child.visits + child.results[node.player]).availableMoves[0]


def random_move(state, player):
    available_moves = get_possible_moves(state, player)
    
    if available_moves:
        return random.choice(available_moves)
    return None, None

def minimax(pieces, stack, depth, alpha, beta, maximizing, player):
    if depth == 0:
        return heuristic(pieces, player)

    moves = get_possible_moves(pieces, player if maximizing else 1 - player)
    if not moves:
        return heuristic(pieces, player)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            snapshot = create_snapshot(pieces, stack)
            affected_piece, flips_made = apply_move(move, player, pieces, stack)
            outcome = check_win_for_piece(affected_piece.cell)
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
            affected_piece, flips_made = apply_move(move, 1 - player, pieces, stack)
            outcome = check_win_for_piece(affected_piece.cell)
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
