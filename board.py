from config import CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT


class Board:
    def __init__(self, canvas, x_offset, y_offset):
        self.canvas = canvas
        self.x_offset = x_offset
        self.y_offset = y_offset
        # сетка ячеек
        self.cells = [[{'color': 'white', 'occupied': False} for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def draw_board(self):
        """Отображает доску с текущими цветами ячеек."""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = self.cells[y][x]['color']
                self.canvas.create_rectangle(
                    x * CELL_SIZE + self.x_offset, y * CELL_SIZE + self.y_offset,
                    (x + 1) * CELL_SIZE + self.x_offset, (y + 1) * CELL_SIZE + self.y_offset,
                    fill=color, outline='black'
                )

    def can_place_figure(self, figure):
        """Проверяет, можно ли поместить фигуру в текущее положение."""
        x0, y0 = (figure.x - self.x_offset) // CELL_SIZE, (figure.y - self.y_offset) // CELL_SIZE
        for cell in figure.get_shape_positions():
            x, y = x0 + int(cell[0]), y0 + int(cell[1])
            if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT or self.cells[y][x]['occupied']:
                return False
        return True

    def place_figure_on_board(self, figure):
        """Помечает ячейки занятыми и окрашивает их в цвет фигуры."""
        x0, y0 = (figure.x - self.x_offset) // CELL_SIZE, (figure.y - self.y_offset) // CELL_SIZE
        for cell in figure.get_shape_positions():
            x, y = x0 + int(cell[0]), y0 + int(cell[1])
            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                self.cells[y][x]['color'] = figure.color
                self.cells[y][x]['occupied'] = True
        self.draw_board()

    def clear_board(self):
        """Сбрасывает все ячейки доски."""
        for row in self.cells:
            for cell in row:
                cell['color'] = 'white'
                cell['occupied'] = False
        self.draw_board()
