class Node:
    def __init__(self, state, parent = None , action = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def expand(self, problem):
        reachable = []
        for action in problem.actions(self.state):
            reachable.append(self.child_node(problem, action))
        return reachable

    def child_node(self, problem, action):
        next = problem.result(self.state, action)
        return Node(next, self, action, problem.path_cost(self.path_cost, self.state, action, next))
        ##  ^^stato prossimo, nodo padre, azione, costo del cammino^^

    def path(self):
        path = [self]
        node = self
        while node.parent:              ##se il nodo ha un padre
            node = node.parent
            path.append(node)           ##aggiungo il nodo padre al path
        return path[::-1]               ##lista di nodi al contrario

    def solution(self):
        actions = []
        for node in self.path():        ##per ogni nodo nel path
            actions.append(node.action) ##aggiungo l'azione
        return actions[1:]              ##ritorno la lista di azioni tranne la prima (None)

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return str(self.state)

