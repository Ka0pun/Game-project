import tkinter as tk
import random
from tkinter import messagebox, simpledialog
import os

class MemoryGame:
    def __init__(self, root, grid_size):
        self.root = root
        self.root.title("Memory Card Matching Game")
        self.grid_size = grid_size
        self.symbols = list(range(self.grid_size**2 // 2)) * 2
        random.shuffle(self.symbols)
        self.buttons = []
        self.flipped = []
        self.score = 0
        self.time_left = 60
        self.high_score = self.load_high_score()
        
        # Load the back image first
        try:
            self.back_image = tk.PhotoImage(file=os.path.join("images", "back.png"))
        except Exception as e:
            print(f"Error loading back.png: {e}")
            # Create a default back image
            self.back_image = tk.PhotoImage(width=64, height=64)
        
        # Load card images
        self.images = self.load_images()
        self.create_score_label()
        self.create_timer_label()
        self.create_board()
        self.start_timer()

    def load_images(self):
        images = []
        for i in range(self.grid_size**2 // 2):
            img_path = os.path.join("images", f"img{i}.png")
            try:
                img = tk.PhotoImage(file=img_path)
                images.append(img)
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
                # Create a default image if loading fails
                default_img = tk.PhotoImage(width=64, height=64)
                images.append(default_img)
        return images

    def load_high_score(self):
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def create_score_label(self):
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.grid(row=0, column=0, columnspan=self.grid_size // 2, pady=(10, 0))

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def create_timer_label(self):
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.grid(row=0, column=self.grid_size // 2, columnspan=self.grid_size // 2, pady=(10, 0))

    def update_timer(self):
        self.timer_label.config(text=f"Time Left: {self.time_left}s")

    def start_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_timer()
            self.root.after(1000, self.start_timer)
        else:
            self.end_game("Time's up! You ran out of time!")

    def create_board(self):
        for row in range(1, self.grid_size + 1):
            button_row = []
            for col in range(self.grid_size):
                btn = tk.Button(self.root, image=self.back_image, width=64, height=64,
                              command=lambda r=row-1, c=col: self.flip_card(r, c))
                btn.grid(row=row, column=col, padx=5, pady=5)
                button_row.append(btn)
            self.buttons.append(button_row)

    def flip_card(self, row, col):
        if len(self.flipped) < 2 and self.buttons[row][col]["image"] == str(self.back_image):
            img_index = self.symbols[row * self.grid_size + col]
            self.buttons[row][col].config(image=self.images[img_index])
            self.flipped.append((row, col))

            if len(self.flipped) == 2:
                self.root.after(1000, self.check_match)

    def check_match(self):
        r1, c1 = self.flipped[0]
        r2, c2 = self.flipped[1]
        idx1 = self.symbols[r1 * self.grid_size + c1]
        idx2 = self.symbols[r2 * self.grid_size + c2]

        if idx1 == idx2:
            self.buttons[r1][c1]["state"] = "disabled"
            self.buttons[r2][c2]["state"] = "disabled"
            self.score += 1
            self.update_score()
        else:
            self.buttons[r1][c1].config(image=self.back_image)
            self.buttons[r2][c2].config(image=self.back_image)

        self.flipped = []

        if all(btn["state"] == "disabled" for row in self.buttons for btn in row):
            self.end_game(f"Congratulations! You matched all the cards! Final Score: {self.score}")

    def end_game(self, message):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            message += f"\nNew High Score: {self.high_score}!"
        else:
            message += f"\nHigh Score: {self.high_score}"
        messagebox.showinfo("Game Over", message)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    grid_size = simpledialog.askinteger("Grid Size", "Enter grid size (e.g., 4 for 4x4, maximum is 4):", minvalue=2, maxvalue=4)
    if grid_size:
        game = MemoryGame(root, grid_size)
        root.mainloop()
