# Puzzle Solver

## 👨‍💻 Group Members

| Name               | Student ID     |
|--------------------|----------------|
| Abdullah Tariq     | 221378         |
| Abdur Rehman       | 221423         |
| Abdul Majid        | 221399         |

---

## 📄 Project Summary

This project is a **GUI-based AI puzzle solver** for the classic 8-Puzzle (sliding puzzle). The system enables users to input any custom configuration of a puzzle (from 2x2 up to 10x10), select a solving algorithm (A* Search** or Breadth-First Search), and view the solution path in a clear and interactive interface.

The solution includes:

- A modern WPF desktop frontend (C#).
- A Python backend implementing the puzzle-solving logic.
- Communication between the frontend and backend using standard I/O and process handling.
- Support for performance analysis, solution visualization, and error handling.

---

## 🚀 Setup & Run Instructions

### 🧰 Requirements

- **.NET 6.0 or newer** for WPF frontend
- **Python 3.7+**
- Python packages: `numpy` (Install with `pip install numpy`)

### ▶️ Run Instructions

1. Open the solution in **Visual Studio** and set `PuzzleSolverFrontend` as the startup project.
2. Make sure Python is in your system's PATH.
3. Place `puzzle.py`, `state.py`, and `game.py` in the project.
4. Run the WPF application.
5. Enter the puzzle size and values.
6. Choose the solving method (A* or BFS).
7. Click "Solve Puzzle" to see the solution.



## 🧠 AI Techniques Used

### 1. A* Search

- Type: Informed Search (Best-First)
- Heuristic: Manhattan Distance
- Data Structure: Priority Queue
- Why A*?
  - Efficient in finding optimal paths.
  - Significantly reduces search space by using heuristic guidance.
  - Ideal for puzzle-solving where the cost to goal can be estimated accurately.

### 2. Breadth-First Search (BFS)

- Type: Uninformed Search
- Data Structure: FIFO Queue
- Why BFS?
  - Guaranteed to find the shortest path in terms of number of moves.
  - Used as a benchmark to compare with A*.
  - Simple and easy to implement but less efficient for large puzzles.





