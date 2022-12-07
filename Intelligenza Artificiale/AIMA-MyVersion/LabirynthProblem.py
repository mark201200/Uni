import math

from PriorityQueue import PriorityQueue
from State import LabirynthState


class LabirynthProblem:
    def __init__(self, start, goal, labirynthMap):
        self.start = start
        self.goal = goal
        self.map = labirynthMap
        self.mapWidth = len(labirynthMap[0]) - 1
        self.mapHeight = len(labirynthMap) - 1

    def actions(self, state):
        actions = []
        if state.x > 0 and self.map[state.x - 1][state.y] != '#':
            actions.append('left')
        if state.x < self.mapHeight and self.map[state.x + 1][state.y] != '#':
            actions.append('right')
        if state.y > 0 and self.map[state.x][state.y - 1] != '#':
            actions.append('up')
        if state.y < self.mapWidth and self.map[state.x][state.y + 1] != '#':
            actions.append('down')
        return actions

    def result(self, state, action):
        if action == 'left':
            return LabirynthState(state.x - 1, state.y)
        if action == 'right':
            return LabirynthState(state.x + 1, state.y)
        if action == 'up':
            return LabirynthState(state.x, state.y - 1)
        if action == 'down':
            return LabirynthState(state.x, state.y + 1)

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    @staticmethod
    def print_path(nodePath, problem):
        path = []

        for node in nodePath:
            path.append([node.state.x, node.state.y])

        for i in range(0, problem.mapHeight + 1):
            for j in range(0, problem.mapWidth + 1):
                if problem.map[i][j] != '#':
                    if [i, j] in path:
                        print('\x1b[102m' + '   ' + '\x1b[0m', end='')
                    else:
                        print('\x1b[47m' + '   ' + '\x1b[0m', end='')
                else:
                    print('\x1b[40m' + '   ' + '\x1b[0m', end='')
            print()
        print()

    @staticmethod
    def print_progress(node, problem, nodeFrontier, stateExplored):
        nodePath = node.path()
        frontier = []
        explored = []
        path = []
        if isinstance(nodeFrontier, PriorityQueue):
            for (_, node) in nodeFrontier.heap:
                frontier.append([node.state.x, node.state.y])
        else:
            for node in nodeFrontier:
                frontier.append([node.state.x, node.state.y])

        for state in stateExplored:
            explored.append([state.x, state.y])

        for node in nodePath:
            path.append([node.state.x, node.state.y])

        for i in range(0, problem.mapHeight + 1):
            for j in range(0, problem.mapWidth + 1):
                if problem.map[i][j] != '#':
                    if [i, j] in path:
                        print('\x1b[44m' + '   ' + '\x1b[0m', end='')
                    elif [i, j] in frontier:
                        print('\x1b[102m' + '   ' + '\x1b[0m', end='')
                    elif [i, j] in explored:
                        print('\x1b[41m' + '   ' + '\x1b[0m', end='')
                    else:
                        print('\x1b[47m' + '   ' + '\x1b[0m', end='')
                else:
                    print('\x1b[40m' + '   ' + '\x1b[0m', end='')
            print()
        print()

    def h(self, node):
        return abs(node.state.x - self.goal.x) + abs(node.state.y - self.goal.y)
        #return math.dist([node.state.x, node.state.y], [self.goal.x, self.goal.y])

    def g(self, node):
        return len(node.path())
