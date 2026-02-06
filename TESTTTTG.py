import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk
import winsound
import os
import random

# ----------------- SYMBOL INPUT -----------------
while True:
    X = input('What symbol would you like in place of "X"? (NO NUMBERS ALLOWED): ')
    O = input('What symbol would you like in place of "O"? (NO NUMBERS ALLOWED): ')
    if X.isdigit() or O.isdigit():
        print("ERROR!! NO NUMBERS ARE ALLOWED, PLEASE TRY AGAIN")
    else:
        break

players = cycle([(X, "dodgerblue"), (O, "hotpink")])

# ----------------- GAME LOGIC -----------------
class Game:
    def __init__(self):
        self.player = next(players)
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.winner = None

    def valid_move(self, r, c):
        return self.board[r][c] == " " and self.winner is None

    def move(self, r, c):
        mark, _ = self.player
        self.board[r][c] = mark

        if self.check_win(mark):
            self.winner = mark
            return

        if all(cell != " " for row in self.board for cell in row):
            self.winner = "draw"
            return

        self.player = next(players)

    def check_win(self, mark):
        for row in self.board:
            if all(cell == mark for cell in row):
                return True
        for c in range(3):
            if all(self.board[r][c] == mark for r in range(3)):
                return True
        if all(self.board[i][i] == mark for i in range(3)):
            return True
        if all(self.board[i][2 - i] == mark for i in range(3)):
            return True
        return False

    def reset(self):
        self.__init__()

# ----------------- CONFETTI -----------------
class Confetti:
    def __init__(self, window):
        self.window = window
        self.canvas = None
        self.pieces = []

    def start(self):
        if self.canvas:
            self.canvas.destroy()

        self.canvas = tk.Canvas(
            self.window,
            width=self.window.winfo_screenwidth(),
            height=self.window.winfo_screenheight(),
            bg="black",
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0)

        for _ in range(120):
            x = random.randint(0, self.window.winfo_screenwidth())
            y = random.randint(-200, 0)
            size = random.randint(6, 12)
            color = random.choice(
                ["red", "yellow", "blue", "green", "pink", "cyan"]
            )
            piece = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color, outline=""
            )
            self.pieces.append(piece)

        self.animate()
        self.window.after(1500, self.stop)

    def animate(self):
        for p in self.pieces:
            self.canvas.move(p, 0, 6)
        self.window.after(30, self.animate)

    def stop(self):
        if self.canvas:
            self.canvas.destroy()
            self.canvas = None
            self.pieces.clear()

# ----------------- GUI -----------------
class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.attributes("-fullscreen", True)
        self.title("Tic Tac Toe lol")

        # ---------- BACKGROUND ----------
        img_path = os.path.join(os.getcwd(), "fNM5uc.png")
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img = img.resize(
                (self.winfo_screenwidth(), self.winfo_screenheight())
            )
            self.bg_img = ImageTk.PhotoImage(img)
            bg = tk.Label(self, image=self.bg_img)
            bg.place(x=0, y=0, relwidth=1, relheight=1)

        # ---------- MUSIC ----------
        music_path = r"C:\Users\Khanam\ytmp3free.cc_jls-the-club-is-alive-youtubemp3free.org (1).wav"
        if os.path.exists(music_path):
            winsound.PlaySound(
                music_path,
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
            )

        self.bind("<Escape>", lambda e: self.on_close())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.game = Game()
        self.confetti = Confetti(self)

        self.label = tk.Label(
            self,
            text=f"{self.game.player[0]}'s turn",
            font=("Comic Sans MS", 22, "bold"),
            fg=self.game.player[1],
            bg="black"
        )
        self.label.pack(pady=10)

        self.buttons = {}
        board = tk.Frame(self, bg="black")
        board.pack()

        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    board,
                    text=" ",
                    font=("Arial", 48),
                    width=3,
                    command=lambda r=r, c=c: self.click(r, c)
                )
                btn.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[(r, c)] = btn

        tk.Button(
            self,
            text="play again",
            font=("Arial", 14),
            command=self.new_game
        ).pack(pady=10)

    def click(self, r, c):
        if not self.game.valid_move(r, c):
            return

        mark, color = self.game.player
        self.buttons[(r, c)].config(text=mark, fg=color)
        self.game.move(r, c)

        if self.game.winner:
            if self.game.winner == "draw":
                self.label.config(text="draw :/", fg="gray")
            else:
                self.label.config(text=f"{mark} won!!", fg=color)
                self.confetti.start()
        else:
            nxt, clr = self.game.player
            self.label.config(text=f"{nxt}'s turn", fg=clr)

    def new_game(self):
        self.game.reset()
        for b in self.buttons.values():
            b.config(text=" ", fg="black", bg="SystemButtonFace")
        self.label.config(
            text=f"{self.game.player[0]}'s turn",
            fg=self.game.player[1]
        )

    def on_close(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.destroy()

# ----------------- RUN -----------------
if __name__ == "__main__":
    Window().mainloop()

