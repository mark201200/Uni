from PriorityQueue import PriorityQueue
from State import EightPuzzleState


class EightPuzzleProblem:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def actions(self, state):
        actions = []
        coords = state.coords(0)

        if coords[1] > 0:
            actions.append('left')
        if coords[1] < 2:
            actions.append('right')
        if coords[0] > 0:
            actions.append('up')
        if coords[0] < 2:
            actions.append('down')

        return actions

    def result(self, state, action):
        blankCoords = state.coords(0)

        if action == 'left':
            return EightPuzzleState(state.swap(0, state.state[blankCoords[0]][blankCoords[1] - 1]))

        if action == 'right':
            return EightPuzzleState(state.swap(0, state.state[blankCoords[0]][blankCoords[1] + 1]))

        if action == 'up':
            return EightPuzzleState(state.swap(0, state.state[blankCoords[0] - 1][blankCoords[1]]))

        if action == 'down':
            return EightPuzzleState(state.swap(0, state.state[blankCoords[0] + 1][blankCoords[1]]))

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    @staticmethod
    def print_progress(node, *_):
        for i in range(0, 3):
            for j in range(0, 3):
                print(node.state.state[i][j], end=' ')
            print()
        print()

    @staticmethod
    def print_path(nodePath, _):
        for node in nodePath:
            for i in range(0, 3):
                for j in range(0, 3):
                    print(node.state.state[i][j], end=' ')
                print()
            print()
            print("V V V ")

    def h(self, node):
        misplacedTiles = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if node.state.state[i][j] != self.goal.state[i][j]:
                    misplacedTiles += 1
        return misplacedTiles

    def g(self, node):
        return node.path_cost
