from queue import PriorityQueue, Queue
from state import *
import numpy as np

class Game:
    def __init__(self, initial: State, size: int):
        self.initial = initial
        self.size = size

        goal_nums = np.roll(np.arange(size * size), -1).astype(str)
        self.goal = State(goal_nums.reshape(size, size))

        self.goal_digit_pos = {}
        for i in range(size * size):
            x, y = np.where(self.goal.board == str(i))
            self.goal_digit_pos[str(i)] = (int(x[0]), int(y[0]))

    def isGoal(self, someState: State):
        return np.array_equal(someState.board, self.goal.board)

    def getNeighbors(self, state: State):
        neighbors = []
        blank_x, blank_y = state.blank_x, state.blank_y

        moves = [
            ('UP', -1, 0),
            ('DOWN', 1, 0),
            ('LEFT', 0, -1),
            ('RIGHT', 0, 1)
        ]

        for move, dx, dy in moves:
            new_x, new_y = blank_x + dx, blank_y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_board = state.board.copy()
                new_board[blank_x, blank_y], new_board[new_x, new_y] = \
                    new_board[new_x, new_y], new_board[blank_x, blank_y]

                neighbors.append(State(
                    new_board,
                    level=state.level + 1,
                    parent=state,
                    move=move
                ))

        return neighbors

    def search(self, method="astar"):
        if self.isGoal(self.initial):
            return []

        explored = set()

        if method == "astar":
            frontier = PriorityQueue()
            self.initial.getCost(True, self.goal_digit_pos)
            frontier.put(self.initial)
        elif method == "bfs":
            frontier = Queue()
            frontier.put(self.initial)
        else:
            raise ValueError(f"Unsupported method: {method}")

        while not frontier.empty():
            current = frontier.get() if method == "bfs" else frontier.get()

            if self.isGoal(current):
                path = []
                while current.parent:
                    path.append(current.move)
                    current = current.parent
                return path[::-1]

            if current in explored:
                continue
            explored.add(current)

            for neighbor in self.getNeighbors(current):
                if neighbor not in explored:
                    if method == "astar":
                        neighbor.getCost(True, self.goal_digit_pos)
                        frontier.put(neighbor)
                    elif method == "bfs":
                        frontier.put(neighbor)

        return []  # No solution found
