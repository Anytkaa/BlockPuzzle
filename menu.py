import tkinter as tk

from config import MENU_WINDOW_SIZE
from game import Game
from training import show_rules


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.setup_menu()

    def setup_menu(self):
        # Основная настройка меню
        self.root.title("BlockPuzzle")
        self.root.geometry(MENU_WINDOW_SIZE)
        self.root.resizable(False, False)

        # Загрузка и отображение фонового изображения
        self.background_image = tk.PhotoImage(file="assets/menu_background.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Кнопка для начала игры
        start_button = tk.Button(self.root, text="Начать игру", command=self.start_game, font=("helvetica", 25),
                                 fg="magenta3")
        start_button.config(bg="white", width=15, height=2)
        start_button.place(x=470, y=250)

        # Кнопка для открытия правил игры
        training_button = tk.Button(self.root, text="Правила игры", command=self.show_rules, font=("helvetica", 25),
                                    fg="magenta3")
        training_button.config(bg="white", width=15, height=2)
        training_button.place(x=470, y=400)

        # Кнопка для выхода из приложения
        exit_button = tk.Button(self.root, text="Выход", command=self.root.destroy, font=("helvetica", 25),
                                fg="magenta3")
        exit_button.config(bg="white", width=15, height=2)
        exit_button.place(x=470, y=550)

    def start_game(self):
        # Запускает игровую сессию
        self.root.withdraw()  # Скрывает главное окно
        game_window = tk.Toplevel(self.root)
        game = Game(game_window)
        game.start()

    def show_rules(self):
        # Отображает правила игры
        show_rules(self.root)
