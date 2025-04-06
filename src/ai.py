import time
import random
import copy
from pieces import Piece, Stack
from board import graph, DIRECTIONS
from algorithm import get_possible_moves, check_win_for_piece

def random_move(state, player):
    available_moves = get_possible_moves(state, player)

    if available_moves:
        print(f"Movimentos disponíveis: {available_moves}")
        return available_moves[0]
    print("Nenhum movimento disponível")
    return None

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
        # Verifica se o nó está completamente expandido
        return len(self.availableMoves) == 0

    def getUCT(self):
        # Calcula o valor UCT (Upper Confidence Bound for Trees)
        if self.visits == 0:
            return float('inf')
        win_rate = self.results[self.player] / self.visits
        exploration = self.explorationConstant * (2 * (self.parent.visits ** 0.5)) / self.visits
        return win_rate + exploration


class MonteCarloTreeSearch:
    def __init__(self, explorationConstant=1.4, difficulty='Medium'):
        self.explorationConstant = explorationConstant
        self.difficulty = difficulty  # Nível de dificuldade
        self.max_time = self.set_max_time()

    def otherPlayer(self, player):
        # Retorna o jogador oposto
        return 1 - player

    def isTerminal(self, node):
        # Verifica se o estado do nó é terminal (vitória ou derrota)
        return check_win_for_piece(node.state) is not None

    def set_max_time(self):
        # Define o tempo máximo de pesquisa com base na dificuldade
        if self.difficulty == 'Easy':
            return 2  # Menos tempo para dificuldade fácil
        elif self.difficulty == 'Medium':
            return 5  # Tempo moderado para dificuldade média
        else:  # 'Hard'
            return 10  # Mais tempo para dificuldade difícil

    def search(self, initialState, player):
        # Realiza a pesquisa de Monte Carlo
        start_time = time.time()
        root = Node(initialState, player)

        # Executa a pesquisa enquanto o tempo não ultrapassar o limite
        while time.time() - start_time < self.max_time:
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
        # Seleciona o nó filho com o maior valor UCT
        if not node.children:
            return node
        return max(node.children, key=lambda child: child.getUCT())

    def expand(self, node, state, max_depth=3):
        # Expande o nó com novos movimentos
        if len(node.availableMoves) == 0 or (node.parent and node.parent.visits >= max_depth):
            return
        move = node.availableMoves.pop(0)
        newState = copy.deepcopy(state)

        action, cell = move
        if action == "place":
            new_piece = Piece(node.player)
            cell.piece = new_piece
            newState.pieces.append(new_piece)

        childNode = Node(newState, self.otherPlayer(node.player), node)
        node.children.append(childNode)

    def simulation(self, node, state, maxSimulations=50):
        # Simulação para explorar um possível resultado de um movimento
        simulations = 0
        while not self.isTerminal(node) and simulations < maxSimulations:
            moves = node.getAvailableMoves()
            if not moves:
                break
            move = random.choice(moves)
            action, cell = move
            if action == "place":
                new_piece = Piece(node.player)
                cell.piece = new_piece
                state.pieces.append(new_piece)
            node = Node(state, self.otherPlayer(node.player), node)
            simulations += 1
        return node.parent.player if node.parent else 0
    
    def backpropagate(self, node, score):
        # Propaga o resultado da simulação de volta pelos nós pais
        while node is not None:
            node.visits += 1
            node.results[score] += 1
            node = node.parent

    def getBestMove(self, node):
        if not node.children:
            return None
        for child in node.children:
            for move in child.availableMoves:
                return move 
        return None

