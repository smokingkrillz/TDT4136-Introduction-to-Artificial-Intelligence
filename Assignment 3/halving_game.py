import math

State = tuple[int, int]  # (player, number)
Action = str  # '--' or '/2'


class Game:
    def __init__(self, N: int):
        self.N = N

    def initial_state(self) -> State:
        return 0, self.N  # P1 starts

    def to_move(self, state: State) -> int:
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        _, number = state
        actions = []
        if number > 0:
            if number - 1 >= 0:
                actions.append('--')
            if number // 2 >= 0:
                actions.append('/2')
        return actions

    def result(self, state: State, action: Action) -> State:
        _, number = state
        if action == '--':
            return (self.to_move(state) + 1) % 2, number - 1
        else:
            return (self.to_move(state) + 1) % 2, number // 2

    def is_terminal(self, state: State) -> bool:
        _, number = state
        return number == 0

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        # If it's player's turn, that means the *other* player made the last move and won
        return 1 if self.to_move(state) == player else -1

    def print(self, state: State):
        _, number = state
        print(f'The number is {number} and ', end='')
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print('P1 won')
            else:
                print('P2 won')
        else:
            print(f'it is P{self.to_move(state) + 1}\'s turn')


def minimax_search(game: Game, state: State) -> Action | None:
    player = game.to_move(state)

    def max_value(s: State) -> float:
        if game.is_terminal(s):
            return game.utility(s, player)
        v = -math.inf
        for a in game.actions(s):
            v = max(v, min_value(game.result(s, a)))
        return v

    def min_value(s: State) -> float:
        if game.is_terminal(s):
            return game.utility(s, player)
        v = math.inf
        for a in game.actions(s):
            v = min(v, max_value(game.result(s, a)))
        return v

    best_action = None
    best_value = -math.inf
    for a in game.actions(state):
        v = min_value(game.result(state, a))
        if v > best_value:
            best_value = v
            best_action = a
    return best_action


if __name__ == "__main__":
    # Run the halving game
    game = Game(5)
    state = game.initial_state()
    game.print(state)

    while not game.is_terminal(state):
        player = game.to_move(state)
        action = minimax_search(game, state)
        print(f'P{player + 1}\'s action: {action}')
        state = game.result(state, action)
        game.print(state)
