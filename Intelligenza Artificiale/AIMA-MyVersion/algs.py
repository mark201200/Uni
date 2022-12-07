from LabirynthProblem import LabirynthProblem
from Node import Node
from PriorityQueue import PriorityQueue


def breadth_first_search(problem, visual=False):
    frontier = [Node(problem.start)]
    explored = {problem.start}  ##in explored ci sono gli STATI, non i nodi. non so se mantenerlo così. in caso fai node(problemstart)
    iteration = 0

    while frontier:
        iteration += 1
        node = frontier.pop(0)

        if visual:
            problem.print_progress(node, problem, frontier, explored)

        if problem.goal_test(node.state):
            if visual:
                problem.print_path(node.path(), problem)
            print("Finished in ", iteration, " iterations")
            return node

        for neighbor in node.expand(
                problem):  ##appende i nodi raggiungibili da node alla frontiera (extend sarebbe concatenazione)
            if neighbor.state not in explored:
                explored.add(neighbor.state)
                frontier.append(neighbor)

    return None


def depth_first_search(problem, visual=False):
    frontier = [Node(problem.start)]
    explored = {problem.start}  ##in explored ci sono gli STATI, non i nodi. non so se mantenerlo così. in caso fai node(problemstart)
    iteration = 0

    while frontier:
        iteration += 1
        node = frontier.pop(-1)

        if visual:
            problem.print_progress(node, problem, frontier, explored)

        if problem.goal_test(node.state):
            if visual:
                problem.print_path(node.path(), problem)
            print("Finished in ", iteration, " iterations")
            return node

        for neighbor in node.expand(problem):  ##appende i nodi raggiungibili da node alla frontiera (extend sarebbe concatenazione)
            if neighbor.state not in explored:
                explored.add(neighbor.state)
                frontier.append(neighbor)

    return None


def best_first_search(problem, f, visual=False):
    iteration = 0
    frontier = PriorityQueue('min', f)
    frontier.append(Node(problem.start))
    explored = {problem.start}

    while frontier:
        iteration += 1
        node = frontier.pop()

        if visual:
            problem.print_progress(node, problem, frontier, explored)

        if problem.goal_test(node.state):
            if visual:
                problem.print_path(node.path(), problem)
            print("Finished in ", iteration, " iterations")
            return node

        for neighbor in node.expand(problem):
            if neighbor.state not in explored:
                explored.add(neighbor.state)
                frontier.append(neighbor)

    return None
