import random

class Figure:
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

    def __init__(self, type=None):
        if type is None:
            self.type = random.choice(list(self.figures.keys()))
        else:
            self.type = type
        self.color = self.figures[self.type]['color']
        self.shape = self.figures[self.type]['shape']
        self.size = self.figures[self.type]['size']

    def get_shape_positions(self, x, y):
        """Calculate the absolute board positions of the figure based on top-left corner (x, y)."""
        return [(x + int(pos[0]), y + int(pos[1])) for pos in self.shape]
