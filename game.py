import tkinter as tk
from board import Board
from ui import center_window, show_game_over_message

class Game:
    def __init__(self, root):
        self.root = root
        self.board = Board(self.root, self.game_over_callback)

    def start(self):
        self.board.setup()
        self.board.draw_board()

    def game_over_callback(self):
        show_game_over_message(self.root)
