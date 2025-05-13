import tkinter as tk
import random
from tkinter import messagebox, simpledialog

class MemoryGame:
    def __init__(self, root, grid_size):
        self.root = root
        self.root.title("NEW Memory Card Matching Game")
        self.grid_size = grid_size  # User-defined grid size
        self.symbols = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:self.grid_size**2 // 2] * 2
        random.shuffle(self.symbols)
        self.buttons = []
        self.flipped = []
        self.score = 0  # Initialize score
        self.create_score_label()  # Create score label
        self.create_board()

    def create_score_label(self):
        """Create a label to display the score."""
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.grid(row=0, column=0, columnspan=self.grid_size, pady=(10, 0))

    def update_score(self):
        """Update the score label."""
        self.score_label.config(text=f"Score: {self.score}")

    def create_board(self):
        for row in range(1, self.grid_size + 1):  # Adjust row index to account for score label
            button_row = []
            for col in range(self.grid_size):
                btn = tk.Button(self.root, text="", width=8, height=4,
                                command=lambda r=row - 1, c=col: self.flip_card(r, c))
                btn.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(btn)
            self.buttons.append(button_row)

    def flip_card(self, row, col):
        if len(self.flipped) < 2 and not self.buttons[row][col]["text"]:
            self.buttons[row][col]["text"] = self.symbols[row * self.grid_size + col]
            self.flipped.append((row, col))

            if len(self.flipped) == 2:
                self.root.after(1000, self.check_match)

    def check_match(self):
        r1, c1 = self.flipped[0]
        r2, c2 = self.flipped[1]

        if self.symbols[r1 * self.grid_size + c1] == self.symbols[r2 * self.grid_size + c2]:
            self.buttons[r1][c1]["state"] = "disabled"
            self.buttons[r2][c2]["state"] = "disabled"
            self.score += 1  # Increment score for a match
            self.update_score()
        else:
            self.buttons[r1][c1]["text"] = ""
            self.buttons[r2][c2]["text"] = ""

        self.flipped = []

        if all(btn["state"] == "disabled" for row in self.buttons for btn in row):
            messagebox.showinfo("Congratulations!", f"You matched all the cards! Final Score: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    grid_size = simpledialog.askinteger("Grid Size", "Enter grid size (e.g., 4 for 4x4):", minvalue=2, maxvalue=10)
    if grid_size:
        game = MemoryGame(root, grid_size)
        root.mainloop()