from copy import deepcopy
import math
from halving_game import minimax_search
import time

def alphabeta_search(game, state):
    """Return the best action using alpha–beta pruning."""
    player = game.to_move(state)

    def max_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player)
        v = -math.inf
        for a in game.actions(s):
            v = max(v, min_value(game.result(s, a), alpha, beta))
            if v >= beta:
                return v  # β cutoff
            alpha = max(alpha, v)
        return v

    def min_value(s, alpha, beta):
        if game.is_terminal(s):
            return game.utility(s, player)
        v = math.inf
        for a in game.actions(s):
            v = min(v, max_value(game.result(s, a), alpha, beta))
            if v <= alpha:
                return v  # α cutoff
            beta = min(beta, v)
        return v

    best_score = -math.inf
    best_action = None
    alpha, beta = -math.inf, math.inf
    for a in game.actions(state):
        v = min_value(game.result(state, a), alpha, beta)
        if v > best_score:
            best_score = v
            best_action = a
        alpha = max(alpha, best_score)
    return best_action



State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')

game = Game()
state = game.initial_state()


print("\n=== Tic-tac-toe first move timing comparison ===")
t0 = time.perf_counter()
first_move_minimax = minimax_search(game, state)
t1 = time.perf_counter()

t2 = time.perf_counter()
first_move_alphabeta = alphabeta_search(game, state)
t3 = time.perf_counter()

print(f"Minimax first move: {first_move_minimax}, time = {t1 - t0:.6f} seconds")
print(f"Alpha-Beta first move: {first_move_alphabeta}, time = {t3 - t2:.6f} seconds")
print()

while not game.is_terminal(state):
    player = game.to_move(state)
    action = alphabeta_search(game, state)
    print(f'P{player + 1} plays {action}')
    state = game.result(state, action)
    game.print(state)
