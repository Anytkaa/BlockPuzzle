import random

from config import CELL_SIZE

figures = {
    'O': {'color': 'Turquoise2', 'shape': ['02', '12', '01', '11'], 'size': (2, 2)},
    'I': {'color': 'palegreen', 'shape': ['00', '01', '02', '03'], 'size': (1, 4)},
    'J': {'color': 'coral', 'shape': ['01', '11', '21', '22'], 'size': (2, 3)},
    'L': {'color': 'red2', 'shape': ['21', '11', '01', '00'], 'size': (2, 3)},
    'T': {'color': 'gold', 'shape': ['11', '01', '21', '10'], 'size': (3, 2)},
    'Z': {'color': 'Lightskyblue', 'shape': ['01', '11', '10', '20'], 'size': (3, 2)},
    'S': {'color': 'hotpink1', 'shape': ['10', '11', '01', '02'], 'size': (3, 2)},
    'E': {'color': 'orchid1', 'shape': ['00', '01', '02', '10'], 'size': (3, 2)},
    'G': {'color': 'brown1', 'shape': ['01', '11', '21', '02'], 'size': (2, 3)},
    'I_vert': {'color': 'cornflowerblue', 'shape': ['00', '10', '20', '30'], 'size': (1, 4)},
    'T_right': {'color': 'seagreen1', 'shape': ['10', '11', '12', '01'], 'size': (3, 2)},
    'T_vnis': {'color': 'mediumpurple1', 'shape': ['01', '11', '21', '12'], 'size': (2, 3)}
}


class Figure:

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
