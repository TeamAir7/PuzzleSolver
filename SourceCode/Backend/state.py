import numpy as np

class State:
    def __init__(self, board: np.ndarray, level=0, parent=None, move=None):
        self.board = board
        self.level = level
        self.parent = parent
        self.move = move
        self.cost = level  # Initial cost is just the path length
        
        # Find blank (0) position
        x, y = np.where(board == '0')
        self.blank_x, self.blank_y = int(x[0]), int(y[0])

    def __hash__(self):
        return hash(str(self.board))

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    # Comparison methods for priority queue
    def __lt__(self, other):
        return self.cost < other.cost

    def getCost(self, heuristic=False, goal_digit_pos:dict={}):
        self.cost = self.level  # Start with path cost
        
        if heuristic and goal_digit_pos:
            manhattan = 0
            # Calculate Manhattan distance for all tiles except blank (0)
            for i in range(1, self.board.size):
                x, y = np.where(self.board == str(i))
                goal_x, goal_y = goal_digit_pos[str(i)]
                manhattan += abs(int(x[0]) - goal_x) + abs(int(y[0]) - goal_y)
            self.cost += manhattan
            
        return self.cost

    def getParent(self):
        return self.parent

    def getMove(self):
        return self.move
