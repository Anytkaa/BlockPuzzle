import tkinter as tk
from tkinter import PhotoImage, Button

from board import Board
from config import CELL_SIZE, GAME_WINDOW_SIZE, FIGURES_COUNT, POINTS_PER_FIGURE, FIGURE_GAP, POINTS_PER_ROW, \
    POINTS_PER_COL, BOARD_X_OFFSET, BOARD_Y_OFFSET, FIGURE_LIST_Y_OFFSET
from figures import Figure
from gameover import GameOverWindow


class Game:
    """Основной класс, управляющий игровым процессом.
    Этот класс инициализирует игровое поле, управляет событиями игры
    (например, нажатиями кнопок мыши для перемещения фигур),
    обрабатывает логику начала новой игры, сброса текущей игры и окончания игры.
    Также управляет выводом счета и обновлением игровых элементов."""

    def __init__(self, master):
        # Переменные
        self.score = 0
        self.figures_in_sidebar = []  # Список фигур в боковой панели
        self.figures = []  # Список всех невставленных фигур
        self.active_figure = None  # Активная фигура для перемещения, теперь это ссылка на объект
        # координаты смещения мышки относительно координат активной фигуры
        self.offset_x = None
        self.offset_y = None
        # Внешний вид окна
        self.master = master
        self.master.title("BlockPuzzle Game")
        self.master.geometry(GAME_WINDOW_SIZE)
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Создание канваса для игрового поля
        self.canvas = tk.Canvas(self.master, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Загрузка и отображение фонового изображения
        self.background_image = PhotoImage(file="assets/game_background.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Инициализация доски с смещениями
        self.board = Board(self.canvas, BOARD_X_OFFSET, BOARD_Y_OFFSET)
        self.board.draw_board()

        # Создание метки для отображения счета
        self.score_label = tk.Label(self.master, text="Счет: 0", font=("tahoma", 30), bg="#E0FFFF")
        self.score_label.place(x=30, y=30)

        # Кнопки управления игрой
        self.exit_button = Button(self.master, text="Выход", command=self.master.destroy, font=("helvetica", 20),
                                  fg="magenta3")
        self.exit_button.config(bg='white', width=10, height=2)
        self.exit_button.place(x=1000, y=35)

        self.reset_button = Button(self.master, text="Новая игра", command=self.reset_game, font=("helvetica", 20),
                                   fg="magenta3")
        self.reset_button.config(bg='white', width=10, height=2)
        self.reset_button.place(x=1000, y=205)

        # Вызов методов инициализации
        self.setup_bindings()
        self.create_new_set_of_figures()
        self.start()

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
            fig = Figure(tag, self.canvas, FIGURE_LIST_Y_OFFSET, y_offset)
            self.figures_in_sidebar.append(fig)
            self.figures.append(fig)
            self.draw_figure_widget(fig, FIGURE_LIST_Y_OFFSET, y_offset)
            y_offset += fig.size[1] * CELL_SIZE + FIGURE_GAP

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
            self.draw_figure_widget(fig, FIGURE_LIST_Y_OFFSET, y_offset)
            y_offset += fig.size[1] * CELL_SIZE + FIGURE_GAP

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
                removed_rows, removed_cols = self.board.place_figure_on_board(self.active_figure)
                # повышаем счёт
                self.update_score(POINTS_PER_FIGURE + removed_rows * POINTS_PER_ROW + removed_cols * POINTS_PER_COL)
                self.figures.remove(self.active_figure)
                self.active_figure.clear()  # удаляем помещённую фигуру
                if len(self.figures) == 0:  # если поместили вне фигуры
                    self.active_figure = None
                    self.create_new_set_of_figures()
                # Новая проверка проигрыша. Ведь можно поставить фигуру так, что места под другие уже не будет.
                elif self.board.check_game_over(self.figures):
                    self.show_game_over_message()  # Показать сообщение о проигрыше
            self.active_figure = None

    def update_score(self, amount):
        self.score += amount
        self.score_label.config(text=f"Счет: {self.score}")

    def reset_game(self):
        self.board.clear_board()
        self.score = 0
        self.update_score(0)
        for fig in self.figures:
            fig.clear()
        self.active_figure = None
        self.figures.clear()
        self.figures_in_sidebar.clear()
        self.create_new_set_of_figures()
        self.start()

    def show_game_over_message(self):
        GameOverWindow(self.master, self.score, self.reset_game)
        pass

    def on_close(self):
        """Обрабатывает закрытие окна игры и повторно открывает главное меню."""
        self.master.destroy()  # Уничтожение текущего окна
