"""
shape_sudoku_solver.py
======================

A minimal yet scalable solver for shape Sudoku (Latin-square-style) puzzles with a simple UI.
Each row and column must contain exactly one of each symbol. No sub-grid constraints are assumed.

This version uses a GUI built with tkinter where users can enter puzzle values manually.

Usage:
    Run the script and enter values (1‥N) in the grid. Leave empty cells blank or zero.
    Click 'Solve' to fill in the solution.

"""
from __future__ import annotations

from typing import List, Optional, Tuple, Sequence
import tkinter as tk
from tkinter import messagebox

Grid = List[List[int]]  # 0 == empty; otherwise 1‥N


def find_empty(grid: Grid) -> Optional[Tuple[int, int]]:
    n = len(grid)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                return r, c
    return None


def is_valid(grid: Grid, row: int, col: int, val: int) -> bool:
    n = len(grid)
    if any(grid[row][c] == val for c in range(n)):
        return False
    if any(grid[r][col] == val for r in range(n)):
        return False
    return True


def solve(grid: Grid) -> bool:
    empty = find_empty(grid)
    if empty is None:
        return True
    row, col = empty
    n = len(grid)
    for val in range(1, n + 1):
        if is_valid(grid, row, col, val):
            grid[row][col] = val
            if solve(grid):
                return True
            grid[row][col] = 0
    return False


class SudokuUI:
    def __init__(self, master, size=5):
        self.master = master
        self.size = size
        self.entries = [[tk.Entry(master, width=3, justify='center', font=('Arial', 18))
                         for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                self.entries[r][c].grid(row=r, column=c, padx=2, pady=2)

        solve_btn = tk.Button(master, text="Solve", command=self.solve_puzzle)
        solve_btn.grid(row=size, column=0, columnspan=size, pady=10)

    def get_grid(self) -> Grid:
        grid = []
        for row in self.entries:
            grid_row = []
            for cell in row:
                val = cell.get().strip()
                grid_row.append(int(val) if val.isdigit() else 0)
            grid.append(grid_row)
        return grid

    def set_grid(self, grid: Grid) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.entries[r][c].delete(0, tk.END)
                if grid[r][c] != 0:
                    self.entries[r][c].insert(0, str(grid[r][c]))

    def solve_puzzle(self):
        grid = self.get_grid()
        if solve(grid):
            self.set_grid(grid)
        else:
            messagebox.showinfo("No Solution", "This puzzle has no valid solution.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Shape Sudoku Solver")
    app = SudokuUI(root, size=5)  # Change size here for 4x4, 6x6, etc.
    root.mainloop()