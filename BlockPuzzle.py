import tkinter as tk
import random
from tkinter import Label, Button, Canvas, messagebox, Toplevel, PhotoImage

# Global variables
CELL_SIZE = 60
BOARD_WIDTH = 9
BOARD_HEIGHT = 9
SCORE = 0
selected_figure_ids = []
figure_ids = []
placed_figures_count = 0
occupied_cells = {}
original_coords = {}
start_x = 0  # Начальная позиция X для новой фигуры
start_y = 0  # Начальная позиция Y для новой фигуры
ROWS = 10
COLS = 10
board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

# Определение цветов и фигур
colors = {
    'O': 'Turquoise2',
    'I': 'palegreen',
    'J': 'coral',
    'L': 'red2',
    'T': 'gold',
    'Z': 'Lightskyblue',
    'S': 'hotpink1',
    'E': 'orchid1',
    'G': 'brown1',
    'I_vert': 'cornflowerblue',
    'T_right': 'seagreen1',
    'T_vnis': 'mediumpurple1'
}

figures = {
    'O': ['02', '12', '01', '11'],
    'I': ['00', '01', '02', '03'],
    'J': ['01', '11', '21', '22'],
    'L': ['21', '11', '01', '00'],
    'T': ['11', '01', '21', '10'],
    'Z': ['01', '11', '10', '20'],
    'S': ['10', '11', '01', '02'],
    'E': ['00', '01', '02', '10'],
    'G': ['01', '11', '21', '02'],
    'I_vert': ['00', '10', '20', '30'],
    'T_right': ['10', '11', '12', '01'],
    'T_vnis': ['01', '11', '21', '12'],
}


def start_game():
    global SCORE, figure_ids, occupied_cells, placed_figures_count, selected_figure_ids, start_x, start_y, board

    def exit_game():
        reset_game()
        root.destroy()

    def center_window(window, offset_y=50):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2) - offset_y
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_new_figure():
        return random.choice(['O', 'I', 'J', 'L', 'T', 'Z', 'S', 'E', 'G', 'I_vert', 'T_right', 'T_vnis'])

    def update_score(amount):
        global SCORE
        SCORE += amount
        score_label.config(text=str(SCORE))

    def draw_board():
        board_canvas.delete("cells")
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = "white"  # Цвет по умолчанию для клеток
                board_canvas.create_rectangle(
                    x * CELL_SIZE + BOARD_X_OFFSET, y * CELL_SIZE + BOARD_Y_OFFSET,
                    (x + 1) * CELL_SIZE + BOARD_X_OFFSET, (y + 1) * CELL_SIZE + BOARD_Y_OFFSET,
                    fill=color, outline="black", tags="cells"
                )

    def draw_figure(figure, x, y):
        figure_list = []
        for cell in figures[figure]:
            figure_id = board_canvas.create_rectangle(
                (int(cell[0]) + x) * CELL_SIZE + BOARD_X_OFFSET,  # Adjust x-coordinate
                (int(cell[1]) + y) * CELL_SIZE + BOARD_Y_OFFSET,
                (int(cell[0]) + x + 1) * CELL_SIZE + BOARD_X_OFFSET,  # Adjust x-coordinate
                (int(cell[1]) + y + 1) * CELL_SIZE + BOARD_Y_OFFSET,
                fill=colors[figure], outline="black"
            )
            figure_list.append(figure_id)
        figure_ids.append(figure_list)

    def is_position_valid(figure_id, x, y):
        # Проверяем, свободны ли клетки для размещения фигуры
        return (x, y) not in occupied_cells

    def can_place_figure(figure, x, y):
        # Проверяем, можно ли разместить фигуру на доске
        for cell in figures[figure]:
            cell_x = int(cell[0]) + x
            cell_y = int(cell[1]) + y
            # Если координаты клетки выходят за границы доски или уже заняты, возвращаем False
            if cell_x < 0 or cell_x >= BOARD_WIDTH or cell_y < 0 or cell_y >= BOARD_HEIGHT or (
                    cell_x, cell_y) in occupied_cells:
                return False
        # Если все клетки для фигуры свободны и в пределах доски, возвращаем True
        return True

    def place_figure_on_board(figure_id, x, y):
        # Размещаем фигуру на доске и обновляем occupied_cells
        cell_x = (x - BOARD_X_OFFSET) // CELL_SIZE
        cell_y = (y - BOARD_Y_OFFSET) // CELL_SIZE
        if is_position_valid(figure_id, cell_x, cell_y):
            occupied_cells[(cell_x, cell_y)] = figure_id
        else:
            # Если фигура размещена на занятые клетки, возвращаем ее на исходное место
            board_canvas.coords(figure_id, original_coords[figure_id])

    def remove_complete_lines():
        global SCORE, figure_ids, occupied_cells
        # Создаем список для хранения индексов строк и столбцов, которые нужно удалить
        rows_to_delete = set()
        cols_to_delete = set()

        # Проверяем каждую строку на наличие 9 заполненных клеток
        for y in range(BOARD_HEIGHT):
            if all((x, y) in occupied_cells for x in range(BOARD_WIDTH)):
                rows_to_delete.add(y)

        # Проверяем каждый столбец на наличие 9 заполненных клеток
        for x in range(BOARD_WIDTH):
            if all((x, y) in occupied_cells for y in range(BOARD_HEIGHT)):
                cols_to_delete.add(x)

        # Удаляем заполненные строки и столбцы
        for y in rows_to_delete:
            for x in range(BOARD_WIDTH):
                if (x, y) in occupied_cells:
                    board_canvas.delete(occupied_cells[(x, y)])
                    del occupied_cells[(x, y)]
            SCORE += BOARD_WIDTH

        for x in cols_to_delete:
            for y in range(BOARD_HEIGHT):
                if (x, y) in occupied_cells:
                    board_canvas.delete(occupied_cells[(x, y)])
                    del occupied_cells[(x, y)]
            SCORE += BOARD_HEIGHT

        # Обновляем отображение счета
        score_label.config(text=str(SCORE))

    def create_new_set_of_figures():
        global placed_figures_count, original_coords
        placed_figures_count = 0
        old_figure_positions = []
        for figure_list in figure_ids[:-1000]:
            for figure_id in figure_list:
                old_figure_positions.append(board_canvas.coords(figure_id))
        # Если нет предыдущих позиций, начинаем с верхнего левого угла
        last_row_y = max(coord[1] for coord in old_figure_positions) if old_figure_positions else 0
        # Создаем новые фигуры и рисуем их
        new_figures = [create_new_figure() for _ in range(3)]
        for i, figure in enumerate(new_figures):
            draw_figure(figure, BOARD_WIDTH + 1, last_row_y + i * 4)
            placed_figures_count += 1
            if placed_figures_count == 3:
                break

        # После размещения новых фигур на доске, удаляем заполненные линии
        remove_complete_lines()

    def snap_to_grid(selected_figure_id):
        for figure_id in selected_figure_id:
            x1, y1, x2, y2 = board_canvas.coords(figure_id)
            new_x1 = round((x1 - BOARD_X_OFFSET) / CELL_SIZE) * CELL_SIZE + BOARD_X_OFFSET
            new_y1 = round((y1 - BOARD_Y_OFFSET) / CELL_SIZE) * CELL_SIZE + BOARD_Y_OFFSET
            dx = new_x1 - x1
            dy = new_y1 - y1
            board_canvas.move(figure_id, dx, dy)
            # После выравнивания фигуры по сетке, размещаем ее на доске
            place_figure_on_board(figure_id, new_x1, new_y1)

    def release(event):
        global selected_figure_ids, placed_figures_count, original_coords
        if selected_figure_ids:
            for selected_figure_id in selected_figure_ids:
                snap_to_grid(selected_figure_id)
                # Проверяем, находится ли каждая часть фигуры в пределах игрового поля
                for fig_id in selected_figure_id:
                    x1, y1, x2, y2 = board_canvas.coords(fig_id)
                    if not (BOARD_X_OFFSET <= x1 < BOARD_X_OFFSET + BOARD_WIDTH * CELL_SIZE and
                            BOARD_Y_OFFSET <= y1 < BOARD_Y_OFFSET + BOARD_HEIGHT * CELL_SIZE):
                        # Если фигура отпущена за пределами поля, возвращаем ее на исходное место
                        board_canvas.coords(fig_id, original_coords[fig_id])
                        return
                selected_figure_ids = []
                update_score(4)
                remove_complete_lines()  # Удаляем заполненные линии сразу после размещения фигуры
                placed_figures_count += 1
                if placed_figures_count == 3:
                    if check_game_over():  # Проверяем, есть ли место для новой фигуры
                        show_game_over_message()
                        stop_game()
                    else:
                        create_new_set_of_figures()  # Создаем новый набор фигур, если игра не окончена
                        placed_figures_count = 0

    def motion(event):
        global selected_figure_ids, start_x, start_y
        if selected_figure_ids:
            dx = event.x - start_x
            dy = event.y - start_y
            for selected_figure_id in selected_figure_ids:
                for figure_id in selected_figure_id:
                    board_canvas.move(figure_id, dx, dy)
            start_x, start_y = event.x, event.y

    def is_figure_placed_correctly(coords):
        # Используем глобальные переменные для смещения доски
        global BOARD_X_OFFSET, BOARD_Y_OFFSET
        # Размер клетки
        cell_size = 60
        # Проверяем, что координаты фигуры соответствуют границам клеток
        if ((coords[0] - BOARD_X_OFFSET) % cell_size == 0 and
                (coords[1] - BOARD_Y_OFFSET) % cell_size == 0 and
                (coords[2] - BOARD_X_OFFSET) % cell_size == 0 and
                (coords[3] - BOARD_Y_OFFSET) % cell_size == 0):
            return True
        else:
            return False

    original_positions = {}

    def press(event):
        global selected_figure_ids, start_x, start_y
        for figure_list in figure_ids:
            for figure_id in figure_list:
                coords = board_canvas.coords(figure_id)
                if len(coords) == 4:
                    if (event.x > coords[0] and event.x < coords[2]
                            and event.y > coords[1] and event.y < coords[3]):
                        if figure_list in figure_ids[-3:]:
                            selected_figure_ids.append(figure_list)
                            start_x, start_y = event.x, event.y
                            # Проверяем, правильно ли установлена фигура
                            if not is_figure_placed_correctly(coords):
                                messagebox.showerror("Ошибка", "Фигура поставлена неправильно, игра окончена")
                                root.destroy()  # Закрываем окно
                            return

    def draw_figures(old_figure_positions=None):
        new_figures = [create_new_figure() for _ in range(3)]
        if old_figure_positions:
            last_row_y = max(coord[1] for coord in old_figure_positions)
        else:
            last_row_y = 0
        for i, figure in enumerate(new_figures):
            draw_figure(figure, BOARD_WIDTH + 1, last_row_y + i * 3)

    def reset_game():
        global SCORE, figure_ids, occupied_cells, placed_figures_count, selected_figure_ids, start_x, start_y, board
        # Сброс счета
        SCORE = 0
        score_label.config(text=str(SCORE))
        # Удаление всех фигур с доски
        for figure_list in figure_ids:
            for figure_id in figure_list:
                board_canvas.delete(figure_id)
        # Очистка списка идентификаторов фигур, занятых клеток и выбранных фигур
        figure_ids.clear()
        occupied_cells.clear()
        selected_figure_ids.clear()  # Добавлено очищение списка выбранных фигур
        placed_figures_count = 0
        # Сброс начальных координат
        start_x = 0
        start_y = 0
        # Очистка доски
        board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
        # Перерисовка доски
        draw_board()
        # Создание нового набора фигур
        create_new_set_of_figures()
        placed_figures_count = 0

    def check_game_over():
        # Проверяем, есть ли место для размещения всех трех фигур
        for figure in figures:
            has_space = False
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if can_place_figure(figure, x, y):
                        has_space = True
                        break
                if has_space:
                    break
            if not has_space:
                return True  # Если нет места для размещения фигуры, возвращаем True - игра окончена
        return False  # Если есть место для размещения всех трех фигур, возвращаем False - игра продолжается

    background_image = None

    def show_game_over_message():
        global background_image
        # Создаем новое окно
        window = Toplevel()
        window_width = 508
        window_height = 508
        window.geometry(f"{window_width}x{window_height}")
        window.title("Конец игры")
        window.resizable(False, False)

        # Получаем размеры экрана
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Вычисляем координаты для размещения окна по центру
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Размещаем окно по центру
        window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        # Загружаем изображение
        background_image = PhotoImage(file="duck2.png")

        # Создаем метку с фоновым изображением
        background_label = Label(window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Создаем метку с сообщением о конце игры
        label = Label(window, text="Игра окончена! Ваш счет: " + str(SCORE), font=("Arial", 20), fg="red")
        label.pack(padx=10, pady=0)

        # Создаем кнопку для закрытия окна
        button = Button(window, text="OK", command=lambda: [window.destroy(), reset_game()])
        button.pack(padx=70, pady=90)

    def stop_game():
        # Закрываем главное окно, что приведет к завершению игры
        root.destroy()

    # В основном цикле игры после размещения фигуры на доске
    if check_game_over():
        # Код для обработки конца игры, например, отображения сообщения и остановки игры
        show_game_over_message()
        reset_game()
        stop_game()

    root = tk.Toplevel()
    root.geometry("1200x700")
    root.title("BLOCKPUZZLE")
    root.resizable(False, False)

    # Создать основное окно
    board_canvas = tk.Canvas(root, width=1500, height=1500, bg="white")
    board_canvas.pack(side="left")  # Изменено на левую сторону

    image_path = "Group 16.png"  # Укажите путь к вашему изображению
    image = tk.PhotoImage(file=image_path)

    # Отображение изображения на заднем фоне
    board_canvas.create_image(0, 0, anchor="nw", image=image)

    board_canvas.bind("<Button-1>", press)
    board_canvas.bind("<B1-Motion>", motion)
    board_canvas.bind("<ButtonRelease-1>", release)

    # Set board offsets
    BOARD_X_OFFSET = 100
    BOARD_Y_OFFSET = 120  # Adjust this value to move the board lower

    draw_board()
    draw_figures()

    # Создать метку для отображения счета
    score_label = tk.Label(root, text="Счет: 0", font=("tahoma", 40), bg="#E0FFFF")
    score_label.place(x=30, y=30)

    exit_button = tk.Button(root, text="выход", command=exit_game, font=("helvetica", 20), fg="magenta3")
    exit_button.config(bg='white', width=10, height=2)
    exit_button.place(x=1000, y=35)

    reset_button = tk.Button(root, text="Новая игра", command=reset_game, font=("helvetica", 20), fg="magenta3")
    reset_button.config(bg='white', width=10, height=2)
    reset_button.place(x=1000, y=205)

    center_window(root, offset_y=70)
    root.mainloop()


def training():
    def exit_game():
        root.destroy()

    def center_window(window, offset_y=50):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2) - offset_y
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    root = tk.Toplevel()
    root.geometry("1200x700")
    root.title("Правила игры")
    root.resizable(False, False)

    # Загружаем изображение
    image_photo_path = "Group 23.png"  # Укажите путь к вашему изображению

    # Отображаем изображение на вкладке с правилами
    image_photo = tk.PhotoImage(file=image_photo_path)
    label = Label(root, image=image_photo)
    label.pack(fill="both", expand=True)

    exit_button = Button(root, text="Выход", command=exit_game, font=("helvetica", 20), fg="black")
    exit_button.config(bg="white", width=15, height=2)
    exit_button.place(x=900, y=20)

    center_window(root, offset_y=70)
    root.mainloop()


# Create the main window
root = tk.Tk()
root.title("BlockPuzzle")
root.geometry("1200x700")
root.resizable(False, False)


def center_window(window, offset_y=50):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2) - offset_y
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


# Load the image
image_path = "Group 1-7.png"
image = tk.PhotoImage(file=image_path)

# Display the image
label = Label(root, image=image)
label.pack(fill="both", expand=True)

# Create canvas for Tetris figures
tetris_canvas = tk.Canvas(root, width=400, height=1300, bg="white")
tetris_canvas.pack(side="right")

start_button = Button(root, text="Начать игру", command=start_game, font=("helvetica", 25), fg="magenta3")
start_button.config(bg="white", width=15, height=2)
start_button.place(x=470, y=250)

training_button = Button(root, text="Правила игры", command=training, font=("helvetica", 25), fg="magenta3")
training_button.config(bg="white", width=15, height=2)
training_button.place(x=470, y=400)

exit_button = Button(root, text="Выход", command=root.destroy, font=("helvetica", 25), fg="magenta3")
exit_button.config(bg="white", width=15, height=2)
exit_button.place(x=470, y=550)

center_window(root, offset_y=70)
root.mainloop()
