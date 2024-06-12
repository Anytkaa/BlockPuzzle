"""Этот файл определяет конфигурационные переменные, которые используются в других частях программы."""

# Настройка окон
MENU_WINDOW_SIZE = "1200x700"
GAME_WINDOW_SIZE = "1200x700"
RULE_WINDOW_SIZE = "1200x700"

# Настройка игры
CELL_SIZE = 60
BOARD_WIDTH = 9
BOARD_HEIGHT = 9
BOARD_X_OFFSET = 100
BOARD_Y_OFFSET = 120
FIGURE_LIST_Y_OFFSET = BOARD_WIDTH * CELL_SIZE + BOARD_Y_OFFSET + 30
FIGURE_GAP = 20  # Расстояние между фигурами в боковой панели фигур
FIGURES_COUNT = 3  # Количество новых фигур в каждом раунде
POINTS_PER_FIGURE = 4  # Количетво очков начисляемых за каждую поставленную фигуру
POINTS_PER_ROW = BOARD_WIDTH  # Количетво очков начисляемых за каждую завершённую строку
POINTS_PER_COL = BOARD_HEIGHT  # Количетво очков начисляемых за каждый завершённый столбец