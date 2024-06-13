from config import CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT


class Board:
    """Класс управляет игровым полем для пазл-игры.
    Он отвечает за отображение ячеек на игровом полотне,
    проверку возможности размещения фигур в определённых позициях,
    а также за обновление состояния поля при размещении фигур.
    Также включает методы для очистки строки/столбца, когда они полностью заполнены."""

    def __init__(self, canvas, x_offset, y_offset):
        self.canvas = canvas
        self.x_offset = x_offset
        self.y_offset = y_offset
        # сетка ячеек
        self.cells = [[{'color': 'white', 'occupied': False} for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def draw_board(self):
        """Отображает доску c текущими цветами ячеек."""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = self.cells[y][x]['color']
                self.canvas.create_rectangle(
                    x * CELL_SIZE + self.x_offset, y * CELL_SIZE + self.y_offset,
                    (x + 1) * CELL_SIZE + self.x_offset, (y + 1) * CELL_SIZE + self.y_offset,
                    fill=color, outline='black'
                )

    def can_place_figure(self, figure):
        """Проверяет, можно ли поместить фигуру в текущее положение где расположена фигура."""
        # переводим координаты фигуры в номера ячеек
        x0, y0 = round((figure.x - self.x_offset) / CELL_SIZE), round((figure.y - self.y_offset) / CELL_SIZE)
        return self.can_place_figure_in_cells(figure, x0, y0)

    def can_place_figure_in_cells(self, figure, x0, y0):
        """Проверяет, можно ли поместить фигуру в положение, задаваемое base_x base_y координатами ячейки."""
        for cell in figure.get_shape_positions():
            x, y = x0 + int(cell[0]), y0 + int(cell[1])
            if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT or self.cells[y][x]['occupied']:
                return False
        return True

    def place_figure_on_board(self, figure):
        """Помечает ячейки занятыми и окрашивает их в цвет фигуры."""
        x0, y0 = round((figure.x - self.x_offset) / CELL_SIZE), round((figure.y - self.y_offset) / CELL_SIZE)
        for cell in figure.get_shape_positions():
            x, y = x0 + int(cell[0]), y0 + int(cell[1])
            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                self.cells[y][x]['color'] = figure.color
                self.cells[y][x]['occupied'] = True
        return self.remove_complete_lines()

    def clear_board(self):
        """Сбрасывает все ячейки доски."""
        for row in self.cells:
            for cell in row:
                cell['color'] = 'white'
                cell['occupied'] = False
        self.draw_board()

    def check_game_over(self, figures):
        """Проверяет, можно ли разместить хотя бы одну из предложенных фигур на доске."""
        # Перебираем каждую фигуру и проверяем, можно ли её где-то разместить на доске
        for figure in figures:
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if self.can_place_figure_in_cells(figure, x, y):
                        # Возвращаем False, если нашли хотя бы одну фигуру, которую можно разместить
                        return False
        # Если не нашли ни одного подходящего места для размещения какой-либо из фигур, возвращаем True - игра окончена
        return True

    def remove_complete_lines(self):
        """Проверяет все строки и столбцы на полное заполнение и очищает их при необходимости."""
        rows_to_clear = []
        cols_to_clear = []

        # Проверка строк на полное заполнение
        for y in range(BOARD_HEIGHT):
            if all(self.cells[y][x]['occupied'] for x in range(BOARD_WIDTH)):
                rows_to_clear.append(y)

        # Проверка столбцов на полное заполнение
        for x in range(BOARD_WIDTH):
            if all(self.cells[y][x]['occupied'] for y in range(BOARD_HEIGHT)):
                cols_to_clear.append(x)

        # Очистка полностью заполненных строк
        for y in rows_to_clear:
            for x in range(BOARD_WIDTH):
                self.cells[y][x]['color'] = 'white'
                self.cells[y][x]['occupied'] = False

        # Очистка полностью заполненных столбцов
        for x in cols_to_clear:
            for y in range(BOARD_HEIGHT):
                self.cells[y][x]['color'] = 'white'
                self.cells[y][x]['occupied'] = False

        # Перерисовка доски после удаления строк и столбцов
        self.draw_board()

        # Возвращаем количество удаленных строк и столбцов
        return len(rows_to_clear), len(cols_to_clear)
