import random

from config import CELL_SIZE

figures = {
    'O': {'color': 'Turquoise2', 'shape': ['00', '01', '11', '10'], 'size': (2, 2)},
    'I': {'color': 'palegreen', 'shape': ['00', '01', '02', '03'], 'size': (1, 4)},
    'J': {'color': 'coral', 'shape': ['00', '10', '20', '21'], 'size': (3, 2)},
    'L': {'color': 'red2', 'shape': ['21', '11', '01', '00'], 'size': (3, 2)},
    'T': {'color': 'gold', 'shape': ['11', '01', '21', '10'], 'size': (3, 2)},
    'Z': {'color': 'Lightskyblue', 'shape': ['01', '11', '10', '20'], 'size': (3, 2)},
    'S': {'color': 'hotpink1', 'shape': ['10', '11', '01', '02'], 'size': (2, 3)},
    'E': {'color': 'orchid1', 'shape': ['00', '01', '02', '10'], 'size': (2, 3)},
    'G': {'color': 'brown1', 'shape': ['00', '10', '20', '01'], 'size': (3, 2)},
    'I_vert': {'color': 'cornflowerblue', 'shape': ['00', '10', '20', '30'], 'size': (4, 1)},
    'T_right': {'color': 'seagreen1', 'shape': ['10', '11', '12', '01'], 'size': (2, 3)},
    'T_vnis': {'color': 'mediumpurple1', 'shape': ['00', '10', '20', '11'], 'size': (3, 2)}
}


class Figure:
    """Класс представляет собой фигуры, используемые в игре.
    Он содержит данные о типе фигуры, её цвете и форме (координатах составляющих блоков).
    Класс также включает методы для отображения фигуры на канвасе и перемещения её по игровому полю."""

    def __init__(self, tag, canvas=None, x=0, y=0):
        self.tag = tag
        self.type = random.choice(list(figures.keys()))
        self.color = figures[self.type]['color']
        self.shape = figures[self.type]['shape']
        self.size = figures[self.type]['size']
        self.x = x
        self.y = y
        self.canvas = canvas
        self.tags = []

    def move(self, x, y):
        """ Перемещает фигуру на абсолютные координаты (x, y). """
        self.x = x
        self.y = y
        self.redraw()

    def redraw(self):
        """ Перерисовывает фигуру на новых координатах. """
        for tag in self.tags:
            self.canvas.delete(tag)
        self.tags.clear()
        self.draw()

    def draw(self):
        """ Рисует фигуру на текущих координатах. """
        for cell in self.shape:
            cx = self.x + int(cell[0]) * CELL_SIZE
            cy = self.y + int(cell[1]) * CELL_SIZE
            tag = self.canvas.create_rectangle(
                cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
                fill=self.color, outline='black', tags=(self.tag,)
            )
            self.tags.append(tag)
        return self.tags

    def get_shape_positions(self):
        return self.shape

    def clear(self):
        """ Удаляет фигуру с канваса, очищая все связанные с ней теги. """
        for tag in self.tags:
            self.canvas.delete(tag)
        self.tags.clear()  # Очищаем список тегов после удаления всех элементов с канваса
