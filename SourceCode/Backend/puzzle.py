from game import *
import sys
import numpy as np

class Puzzle:

    def main():
        args = sys.argv[1:]

        # Require explicit method
        if not args:
            print("Error: No method specified. Use --astar or --bfs", file=sys.stderr)
            sys.exit(1)
        else:
            method = args[0].lstrip('--').lower()
            if method not in ["astar", "bfs"]:
                print(f"Error: Unsupported method '{method}'. Use --astar or --bfs", file=sys.stderr)
                sys.exit(1)

        try:
            # Prompt the user to enter puzzle size
            size_line = input("Enter puzzle size (e.g. 3 for 3x3): ")
            if not size_line:
                raise ValueError("No input provided for puzzle size")
            size = int(size_line.strip())

            if size < 2 or size > 10:
                raise ValueError("Puzzle size must be between 2 and 10")

            print(f"Enter the {size}x{size} puzzle row by row (space-separated values):")

            input_arr = []
            for i in range(size):
                line = input(f"Row {i+1}: ")
                if not line:
                    raise ValueError(f"Incomplete puzzle - expected {size} rows")
                input_arr.append(line.strip().split())

            if len(input_arr) != size:
                raise ValueError(f"Expected {size} rows, got {len(input_arr)}")
            for row in input_arr:
                if len(row) != size:
                    raise ValueError(f"Each row must have {size} elements")

            arr = np.array(input_arr)

            expected_numbers = set(str(x) for x in range(size * size))
            actual_numbers = set(arr.flatten())
            if actual_numbers != expected_numbers:
                raise ValueError("Puzzle must contain all numbers from 0 to size²-1")

            initial_state = State(arr)
            game = Game(initial_state, size=size)

            print(f"Solving {size}x{size} puzzle using {method.upper()}...", file=sys.stderr)
            path = game.search(method=method)

            if path:
                print("\nSolution:")
                for move in path:
                    print(move)
                print(f"\nTotal moves: {len(path)}", file=sys.stderr)
            else:
                if game.isGoal(initial_state):
                    print("Puzzle is already solved!", file=sys.stderr)
                else:
                    print("No solution found!", file=sys.stderr)

        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)

    if __name__ == "__main__":
        main()
