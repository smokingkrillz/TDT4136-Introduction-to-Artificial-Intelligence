import math
from halving_game import minimax_search
State = tuple[int, list[str | int]]  # (player, buckets or numbers)
Action = str | int  # bucket choice or number choice


class Game:
    def initial_state(self) -> State:
        return 0, ['A', 'B', 'C']  # P1 starts

    def to_move(self, state: State) -> int:
        """Returns the player whose turn it is.
         0 for P1, 1 for P2.
         
         
        
        """
        player, _ = state
        return player

    def actions(self, state: State) -> list[Action]:
        _, actions = state
        return actions

    def result(self, state: State, action: Action) -> State:
        if action == 'A':
            return (self.to_move(state) + 1) % 2, [-50, 50]
        elif action == 'B':
            return (self.to_move(state) + 1) % 2, [3, 1]
        elif action == 'C':
            return (self.to_move(state) + 1) % 2, [-5, 15]
        # If action is an int (Player 2’s move)
        assert isinstance(action, int)
        return (self.to_move(state) + 1) % 2, [action]

    def is_terminal(self, state: State) -> bool:
        _, actions = state
        return len(actions) == 1  # Only one number left

    def utility(self, state: State, player: int) -> float:
        assert self.is_terminal(state)
        _, actions = state
        val = actions[0]
        assert isinstance(val, int)
        # If it's the player's turn, the other just played and got the value
        return val if player == self.to_move(state) else -val

    def print(self, state):
        print(f'The state is {state} and ', end='')
        if self.is_terminal(state):
            print(f'P1\'s utility is {self.utility(state, 0)}')
        else:
            print(f'it is P{self.to_move(state) + 1}\'s turn')



game = Game()
state = game.initial_state()
game.print(state)

while not game.is_terminal(state):
    player = game.to_move(state)
    action = minimax_search(game, state)
    print(f'P{player + 1}\'s action: {action}')
    state = game.result(state, action)
    game.print(state)
