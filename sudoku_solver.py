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
    def __init__(self, master):
        self.master = master
        self.size = 5
        self.entries = []
        self.selected_value = None

        self.size_var = tk.IntVar(value=self.size)
        size_menu = tk.OptionMenu(master, self.size_var, *[i for i in range(3, 10)], command=self.change_size)
        size_menu.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

        self.palette_frame = tk.Frame(master)
        self.palette_frame.grid(row=0, column=2, columnspan=3, pady=5, sticky="ew")

        self.board_frame = tk.Frame(master)
        self.board_frame.grid(row=1, column=0, columnspan=5)

        self.solve_btn = tk.Button(master, text="Solve", command=self.solve_puzzle)
        self.solve_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.reset_btn = tk.Button(master, text="Reset", command=self.reset_board)
        self.reset_btn.grid(row=2, column=2, columnspan=2, pady=10, sticky="ew")

        self.build_palette()
        self.build_grid()

    def build_palette(self):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()
        for val in range(1, self.size + 1):
            btn = tk.Button(self.palette_frame, text=str(val), width=2, font=('Arial', 16),
                            command=lambda v=val: self.select_value(v))
            btn.pack(side="left", padx=2)
        blank_btn = tk.Button(self.palette_frame, text="✕", width=2, font=('Arial', 16),
                              command=lambda: self.select_value(None))
        blank_btn.pack(side="left", padx=2)

    def select_value(self, val: Optional[int]):
        self.selected_value = val

    def build_grid(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.entries = []
        for r in range(self.size):
            row_entries = []
            for c in range(self.size):
                entry = tk.Entry(self.board_frame, width=3, justify='center', font=('Arial', 18))
                entry.grid(row=r, column=c, padx=2, pady=2)
                entry.bind("<Button-1>", self.fill_cell(r, c))
                row_entries.append(entry)
            self.entries.append(row_entries)

    def fill_cell(self, row, col):
        def callback(event):
            self.entries[row][col].delete(0, tk.END)
            if self.selected_value:
                self.entries[row][col].insert(0, str(self.selected_value))
        return callback

    def change_size(self, val):
        self.size = int(val)
        self.build_palette()
        self.build_grid()

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

    def reset_board(self):
        for row in self.entries:
            for cell in row:
                cell.delete(0, tk.END)

    def solve_puzzle(self):
        grid = self.get_grid()
        if solve(grid):
            self.set_grid(grid)
        else:
            messagebox.showinfo("No Solution", "This puzzle has no valid solution.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Shape Sudoku Solver")
    app = SudokuUI(root)
    root.mainloop()