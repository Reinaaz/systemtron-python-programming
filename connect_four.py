
import tkinter as tk
from tkinter import messagebox
import random
import os
import sys

ROWS = 6
COLUMNS = 7

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")

        self.turn = 0
        self.board = [["" for _ in range(COLUMNS)] for _ in range(ROWS)]

        self.mode = "two-player"
        self.player1 = "Player 1"
        self.player2 = "Player 2"
        self.scores = {}

        self.hover_col = None

        self.setup_menu()

    def setup_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()

        tk.Label(self.menu_frame, text="Enter Player 1 Name:").grid(row=0, column=0)
        self.p1_entry = tk.Entry(self.menu_frame)
        self.p1_entry.grid(row=0, column=1)

        tk.Label(self.menu_frame, text="Enter Player 2 Name (leave blank for AI):").grid(row=1, column=0)
        self.p2_entry = tk.Entry(self.menu_frame)
        self.p2_entry.grid(row=1, column=1)

        tk.Button(self.menu_frame, text="Start Game", command=self.start_game).grid(row=2, columnspan=2, pady=10)

    def start_game(self):
        self.player1 = self.p1_entry.get() or "Player 1"
        self.player2 = self.p2_entry.get() or "Computer"
        self.mode = "single-player" if self.player2.lower() == "computer" else "two-player"
        self.scores = {self.player1: 0, self.player2: 0}

        self.menu_frame.destroy()
        self.setup_game_ui()

    def setup_game_ui(self):
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Motion>", self.hover_motion)
        self.canvas.bind("<Leave>", self.hover_leave)

        self.status_label = tk.Label(self.root, text=f"{self.player1}'s Turn (Red)")
        self.status_label.pack()

        self.score_label = tk.Label(self.root, text=f"{self.player1}: 0    {self.player2}: 0")
        self.score_label.pack()

        self.reset_button = tk.Button(self.root, text="Reset Board", command=self.reset_board)
        self.reset_button.pack(pady=5)

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.restart_app)
        self.new_game_button.pack(pady=2)

        self.draw_board()

    def draw_board(self, hover_col=None):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLUMNS):
                x0, y0 = c * 100, r * 100
                x1, y1 = x0 + 100, y0 + 100
                color = "white"
                if self.board[r][c] == "R":
                    color = "red"
                elif self.board[r][c] == "Y":
                    color = "yellow"
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color)

        if hover_col is not None:
            self.canvas.create_rectangle(
                hover_col * 100, 0, hover_col * 100 + 100, 600,
                fill="gray", stipple="gray25", outline=""
            )
            row = self.get_next_open_row(hover_col)
            if row is not None:
                x0, y0 = hover_col * 100, row * 100
                x1, y1 = x0 + 100, y0 + 100
                color = "red" if self.turn == 0 else "yellow"
                self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, outline=color, width=4)

    def click(self, event):
        if self.mode == "single-player" and self.turn == 1:
            return  # Ignore clicks when it's AI's turn

        col = event.x // 100
        if 0 <= col < COLUMNS:
            row = self.get_next_open_row(col)
            if row is not None:
                self.play_turn(row, col, "R" if self.turn == 0 else "Y")

                if self.mode == "single-player" and self.turn == 1 and not self.check_win("R") and not self.check_draw():
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        valid_columns = [c for c in range(COLUMNS) if self.get_next_open_row(c) is not None]
        if valid_columns:
            col = random.choice(valid_columns)
            row = self.get_next_open_row(col)
            if row is not None:
                self.play_turn(row, col, "Y")

    def play_turn(self, row, col, piece):
        self.board[row][col] = piece
        self.draw_board(self.hover_col)

        current_player = self.player1 if self.turn == 0 else self.player2

        if self.check_win(piece):
            self.scores[current_player] += 1
            self.update_score()
            replay = messagebox.askyesno("Game Over", f"{current_player} wins!\nDo you want to play again?")
            if replay:
                self.reset_board()
            else:
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Motion>")
                self.status_label.config(text=f"{current_player} won the game!")
        elif self.check_draw():
            replay = messagebox.askyesno("Game Over", "It's a Draw!\nDo you want to play again?")
            if replay:
                self.reset_board()
            else:
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Motion>")
                self.status_label.config(text="Game Drawn.")
        else:
            self.turn ^= 1
            next_player = self.player1 if self.turn == 0 else self.player2
            self.status_label.config(text=f"{next_player}'s Turn ({'Red' if self.turn == 0 else 'Yellow'})")

    def hover_motion(self, event):
        col = event.x // 100
        if 0 <= col < COLUMNS:
            self.hover_col = col
            self.draw_board(hover_col=col)

    def hover_leave(self, event):
        self.hover_col = None
        self.draw_board()

    def get_next_open_row(self, col):
        for r in reversed(range(ROWS)):
            if self.board[r][col] == "":
                return r
        return None

    def check_win(self, piece):
        for r in range(ROWS):
            for c in range(COLUMNS - 3):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return True
        for c in range(COLUMNS):
            for r in range(ROWS - 3):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return True
        for r in range(3, ROWS):
            for c in range(COLUMNS - 3):
                if all(self.board[r-i][c+i] == piece for i in range(4)):
                    return True
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return True
        return False

    def check_draw(self):
        return all(self.board[0][c] != "" for c in range(COLUMNS))

    def update_score(self):
        self.score_label.config(text=f"{self.player1}: {self.scores[self.player1]}    {self.player2}: {self.scores[self.player2]}")

    def reset_board(self):
        self.board = [["" for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.turn = 0
        self.status_label.config(text=f"{self.player1}'s Turn (Red)")
        self.draw_board(self.hover_col)

    def restart_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()
