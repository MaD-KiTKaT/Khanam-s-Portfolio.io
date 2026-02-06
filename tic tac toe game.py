import tkinter as tk
from itertools import cycle

# X = blue, O = pink, classic
players = cycle([("X", "dodgerblue"), ("O", "hotpink")])

class Game:
    def __init__(self):
        self.player = next(players)
        self.board = [[" " for _ in range(3)] for _ in range(3)]   # using space instead of "" looks cleaner imo
        self.won = None

    def can_play(self, r, c):
        return self.board[r][c] == " " and self.won is None

    def play(self, r, c):
        mark, color = self.player
        self.board[r][c] = mark
        
        if self.check_win(mark):
            self.won = mark
            return True
        
        # check draw
        if all(cell != " " for row in self.board for cell in row):
            self.won = "draw"
            return True
            
        self.player = next(players)
        return False

    def check_win(self, mark):
        # rows
        for row in self.board:
            if row == [mark, mark, mark]:
                return True
        # cols
        for c in range(3):
            if all(self.board[r][c] == mark for r in range(3)):
                return True
        # diags
        if self.board[0][0] == mark and self.board[1][1] == mark and self.board[2][2] == mark:
            return True
        if self.board[0][2] == mark and self.board[1][1] == mark and self.board[2][0] == mark:
            return True
        return False

    def restart(self):
        self.__init__()


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("tic tac toe lol")
        self.game = Game()
        
        self.status = tk.Label(self, text=f"{self.game.player[0]}'s turn", 
                              font=("Comic Sans MS", 22, "bold"),   # yes I did that
                              fg=self.game.player[1])
        self.status.pack(pady=12)

        frame = tk.Frame(self)
        frame.pack()

        self.buttons = {}
        for i in range(3):
            for j in range(3):
                b = tk.Button(frame, text=" ", font=("Arial", 48), width=3,
                             command=lambda x=i, y=j: self.clicked(x, y))
                b.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[(i,j)] = b

        tk.Button(self, text="play again", font=("Arial", 14),
                 command=self.new_game).pack(pady=15)

    def clicked(self, r, c):
        if not self.game.can_play(r, c):
            return

        mark, col = self.game.player
        btn = self.buttons[(r,c)]
        btn["text"] = mark
        btn["fg"] = col

        ended = self.game.play(r, c)

        if self.game.won:
            if self.game.won == "draw":
                self.status["text"] = "draw :/"
                self.status["fg"] = "gray"
            else:
                self.status["text"] = f"{self.game.won} won!!"
                self.status["fg"] = col
                self.highlight_winner()
        else:
            next_mark, next_col = self.game.player
            self.status["text"] = f"{next_mark}'s turn"
            self.status["fg"] = next_col

    def highlight_winner(self):
        if self.game.won == "draw":
            return
        win_color = "yellow"
        for r in range(3):
            for c in range(3):
                if self.game.board[r][c] == self.game.won:
                    self.buttons[(r,c)]["bg"] = win_color

    def new_game(self):
        self.game.restart()
        for b in self.buttons.values():
            b["text"] = " "
            b["fg"] = "black"
            b["bg"] = "SystemButtonFace"
        self.status["text"] = f"{self.game.player[0]}'s turn"
        self.status["fg"] = self.game.player[1]


if __name__ == "__main__":
    root = Window()
    root.mainloop()
