import copy


class LabirynthState:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '(%d, %d)' % (self.x, self.y)

    def __repr__(self):
        return str(self)


class EightPuzzleState:
    def __init__(self, state):
        self.state = state

    def coords(self, item):
        for row in self.state:
            if item in row:
                return self.state.index(row), row.index(item)

    def swap(self, item1, item2):
        newState = copy.deepcopy(self.state)
        item1Coords = self.coords(item1)
        item2Coords = self.coords(item2)
        newState[item1Coords[0]][item1Coords[1]] = item2
        newState[item2Coords[0]][item2Coords[1]] = item1
        return newState

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self.state)
