import tkinter as tk
from game import Game
from ui import center_window

def main():
    root = tk.Tk()
    root.title("BlockPuzzle")
    root.geometry("1200x700")
    root.resizable(False, False)

    game = Game(root)
    game.start()

    center_window(root, offset_y=70)
    root.mainloop()

if __name__ == "__main__":
    main()
