import tkinter as tk
from tkinter import ttk, messagebox, END

# Validate the input allowing only numbers from 1 to 9
def validate_input(P):
    return P == "" or (P.isdigit() and 1 <= int(P) <= 9)

# Check if the initial Sudoku grid is valid
def initial_grid_is_valid(grid):
    for row in range(9):
        for col in range(9):
            val = grid[row][col].get()
            if val and not is_valid_move(grid, row, col, val):
                return False
    return True

# Check if placing a number is valid in the Sudoku grid
def is_valid_move(grid, row, col, number):
    for x in range(9):
        if x != col and grid[row][x].get() == number:
            return False
        if x != row and grid[x][col].get() == number:
            return False

    start_row, start_col = 3 * (row//3), 3 * (col//3)

    for i in range(3):
        for j in range(3):
            r, c = start_row + i, start_col + j
            if (r != row or c != col) and grid[r][c].get() == number:
                return False
    return True

# Solve the Sudoku puzzle using backtracking
def solve(grid, row=0, col=0):
    if col == 9:
        if row == 8:
            print("✔️ Λύση ολοκληρώθηκε!")
            return True
        return solve(grid, row + 1, 0)

    if grid[row][col].get():
        return solve(grid, row, col + 1)

    for num in range(1, 10):
        if is_valid_move(grid, row, col, str(num)):

            grid[row][col].delete(0, END)
            grid[row][col].insert(0, str(num))

            if solve(grid, row, col + 1):
                return True

            # Backtrack Backtrack στο ({row},{col}), αφαιρώ το {num}")

            grid[row][col].delete(0, END)

    # Αν κανένας αριθμός δεν ταιριάζει εδώ
    return False

# Create the entry grid for Sudoku input
def create_entry_grid(root, start_y):
    entries = []
    for row in range(9):
        row_entries = []
        for col in range(9):
            vcmd = root.register(validate_input)
            entry = ttk.Entry(root, width=3, font=('Arial', 18), justify='center', validate='key', validatecommand=(vcmd, '%P'))
            entry.place(x=col*40+60, y=row*40+start_y, width=35, height=35)
            row_entries.append(entry)
        entries.append(row_entries)
    return entries

# Create the button grid for displaying selected solutions
def create_button_grid(root, start_y):
    buttons = []
    for row in range(9):
        button_row = []
        for col in range(9):
            btn = tk.Button(root, text='', font=('Arial', 18), width=3, height=1,
                            command=lambda r=row, c=col: reveal_solution(r, c))
            btn.place(x=col*40+60, y=row*40+start_y, width=35, height=35)
            button_row.append(btn)
        buttons.append(button_row)
    return buttons

# Reveal the selected cell solution
def reveal_solution(row, col):
    if solution_grid:
        output_buttons[row][col].config(text=solution_grid[row][col], bg="lightblue")

# Clear all input and output grids
def clear_all():
    global solution_grid
    solution_grid = None
    for r in range(9):
        for c in range(9):
            grid_entries[r][c].delete(0, END)
            output_buttons[r][c].config(text='', bg='SystemButtonFace')

# Solve the Sudoku and display user-entered numbers directly in buttons
def solve_selected():
    global solution_grid
    if not initial_grid_is_valid(grid_entries):
        messagebox.showinfo("Failure", "Initial state is invalid.")
        return

    # Copy user inputs into a temporary grid
    temp_grid = [[grid_entries[r][c].get() for c in range(9)] for r in range(9)]

    # Temporary Entry class to mimic Entry widget behavior
    class TempEntry:
        def __init__(self, val):
            self.val = val
        def get(self):
            return self.val
        def delete(self, a, b):
            self.val = ''
        def insert(self, a, val):
            self.val = val

    # Prepare temporary entries for solving
    temp_entries = [[TempEntry(temp_grid[r][c]) for c in range(9)] for r in range(9)]

    # Solve the Sudoku
    if solve(temp_entries):
        solution_grid = [[temp_entries[r][c].get() for c in range(9)] for r in range(9)]
        for r in range(9):
            for c in range(9):
                # Display user-entered numbers immediately
                output_buttons[r][c].config(text=temp_grid[r][c] if temp_grid[r][c] else '', bg='SystemButtonFace')
    else:
        messagebox.showinfo("Unsolvable", "This Sudoku puzzle has no solution.")

# Solve and immediately display solutions in the entry grid
def solve_all():
    if not initial_grid_is_valid(grid_entries):
        messagebox.showinfo("Failure", "Initial state is invalid.")
        return

    # Solve directly in the entry widgets
    if solve(grid_entries):
        for r in range(9):
            for c in range(9):
                grid_entries[r][c].config(state='normal')
    else:
        messagebox.showinfo("Unsolvable", "This Sudoku puzzle has no solution.")

root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("480x950")
solution_grid = None

# GUI components
tk.Label(root, text="Input Sudoku").place(x=200, y=0)
grid_entries = create_entry_grid(root, 30)

solve_all_button = ttk.Button(root, text="Solve All", command=solve_all)
solve_all_button.place(x=90, y=400)

solve_button = ttk.Button(root, text="Solve Selected", command=solve_selected)
solve_button.place(x=190, y=400)

clear_button = ttk.Button(root, text="Clear", command=clear_all)
clear_button.place(x=320, y=400)

tk.Label(root, text="Select cells to reveal solution").place(x=140, y=450)
output_buttons = create_button_grid(root, 480)

root.mainloop()