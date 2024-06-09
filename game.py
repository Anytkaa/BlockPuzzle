import tkinter as tk
from board import Board
from config import BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, GAME_WINDOW_SIZE, FIGURES_COUNT, POINTS_PER_FIGURE
from figures import Figure
from gameover import GameOverWindow


class Game:
    def __init__(self, master):
        self.score = 0
        self.master = master
        self.master.title("BlockPuzzle Game")
        self.master.geometry(GAME_WINDOW_SIZE)
        self.canvas = tk.Canvas(self.master, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.board = Board(self.canvas, 100, 120)
        self.score_label = tk.Label(self.master, text="0", font=("Arial", 24))
        self.score_label.pack(side=tk.TOP, pady=20)
        self.figures_in_sidebar = []  # Список фигур в боковой панели
        self.figures = []  # Список всех невставленных фигур
        self.active_figure = None  # Активная фигура для перемещения, теперь это ссылка на объект
        # координаты смещения мышки относительно координат активной фигуры
        self.offset_x = None
        self.offset_y = None
        self.setup_bindings()
        self.create_new_set_of_figures()

    def start(self):
        self.board.draw_board()

    def setup_bindings(self):
        self.canvas.bind("<B1-Motion>", self.motion)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def create_new_set_of_figures(self):
        """Создает новый набор фигур для боковой панели."""
        y_offset = 150
        for idx in range(FIGURES_COUNT):
            tag = f"figure_{idx}"
            fig = Figure(tag, self.canvas, 650, y_offset)
            self.figures_in_sidebar.append(fig)
            self.figures.append(fig)
            self.draw_figure_widget(fig, 650, y_offset)
            y_offset += fig.size[1] * CELL_SIZE + 20

        if self.board.check_game_over(self.figures):
            self.show_game_over_message()  # Показать сообщение о проигрыше

    def draw_figure_widget(self, figure, x, y):
        """Рисует фигуру в боковой панели и привязывает событие нажатия."""
        figure.move(x, y)
        self.canvas.tag_bind(figure.tag, "<Button-1>", lambda event, f=figure: self.pick_figure(event, f))

    def update_figure_display(self):
        """Обновляет отображение боковой панели с фигурами после изменений."""
        y_offset = 150
        for fig in self.figures_in_sidebar:
            self.draw_figure_widget(fig, 650, y_offset)
            y_offset += fig.size[1] * CELL_SIZE + 20

    def pick_figure(self, event, figure):
        """Обработчик выбора фигуры."""
        self.active_figure = figure  # Сделать фигуру активной для перемещения
        # Запоминаем начальное смещение от клика до начальных координат фигуры
        self.offset_x = event.x - figure.x
        self.offset_y = event.y - figure.y

    def motion(self, event):
        """Обрабатывает движение мыши с зажатой кнопкой и выбранной фигурой."""
        if self.active_figure:
            # Рассчитываем новые координаты фигуры с учетом смещения
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y
            # Перемещаем фигуру
            self.active_figure.move(new_x, new_y)

    def release(self, event):
        """Обрабатывает отпускание кнопки мыши."""
        if self.active_figure:  # Если это отпускание произошло при перетаскивании фигуры
            if self.active_figure in self.figures_in_sidebar:  # Если фигура находится в боковой панели
                self.figures_in_sidebar.remove(self.active_figure)  # Удалить фигуру из боковой панели
                self.update_figure_display()  # Обновить отображение боковой панели
            if self.board.can_place_figure(self.active_figure):  # теперь вся информация о фигуре
                # хранится в ней (в объекте), как и должно быть
                self.board.place_figure_on_board(self.active_figure)
                self.figures.remove(self.active_figure)
                if len(self.figures) == 0:
                    self.create_new_set_of_figures()
                self.active_figure.clear()
                self.update_score(POINTS_PER_FIGURE)
            self.active_figure = None

    def update_score(self, amount):
        self.score += amount
        self.score_label.config(text=f"{self.score}")

    def game_over(self):
        pass

    def reset_game(self):
        self.board.clear_board()
        self.score = 0
        self.update_score(0)
        self.start()

    def check_game_over(self):
        pass

    def show_game_over_message(self):
        print("GAME OVER")
        GameOverWindow(self.master, self.score, self.reset_game)
        pass
