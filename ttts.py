import tkinter as tk
from itertools import cycle

# Start with player X, then O
players = cycle([("X", "dodgerblue"), ("O", "hotpink")])

class Game:
    def __init__(self):
        self.player = next(players)
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.winner = None

    def valid_move(self, row, col):
        return self.board[row][col] == " " and self.winner is None

    def move(self, row, col):
        mark, _ = self.player
        self.board[row][col] = mark

        if self.check_win(mark):
            self.winner = mark
            return

        if all(cell != " " for row_ in self.board for cell in row_):
            self.winner = "draw"
            return

        self.player = next(players)

    def check_win(self, mark):
        for row in self.board:
            if all(cell == mark for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == mark for row in range(3)):
                return True
        if all(self.board[i][i] == mark for i in range(3)):
            return True
        if all(self.board[i][2 - i] == mark for i in range(3)):
            return True
        return False

    def reset(self):
        self.__init__()

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("tic tac toe lol")
        self.game = Game()
        self.label = tk.Label(self, text=f"{self.game.player[0]}'s turn", font=("Comic Sans MS", 22, "bold"), fg=self.game.player[1])
        self.label.pack(pady=10)

        self.buttons = {}
        board_frame = tk.Frame(self)
        board_frame.pack()

        for row in range(3):
            for col in range(3):
                btn = tk.Button(board_frame, text=" ", font=("Arial", 48), width=3, command=lambda r=row, c=col: self.click(r, c))
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[(row, col)] = btn

        tk.Button(self, text="play again", font=("Arial", 14), command=self.new_game).pack(pady=12)

    def click(self, row, col):
        if not self.game.valid_move(row, col):
            return

        mark, color = self.game.player
        self.buttons[(row, col)].config(text=mark, fg=color)
        self.game.move(row, col)

        if self.game.winner:
            if self.game.winner == "draw":
                self.label.config(text="draw :/", fg="gray")
            else:
                self.label.config(text=f"{mark} won!!", fg=color)
                self.highlight()
        else:
            next_mark, next_color = self.game.player
            self.label.config(text=f"{next_mark}'s turn", fg=next_color)

    def highlight(self):
        for row in range(3):
            for col in range(3):
                if self.game.board[row][col] == self.game.winner:
                    self.buttons[(row, col)].config(bg="yellow")

    def new_game(self):
        self.game.reset()
        for btn in self.buttons.values():
            btn.config(text=" ", fg="black", bg="SystemButtonFace")
        self.label.config(text=f"{self.game.player[0]}'s turn", fg=self.game.player[1])

if __name__ == "__main__":
    Window().mainloop()
