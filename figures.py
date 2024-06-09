import random


class Figure:
    figures = {
        'O': {'color': 'Turquoise2', 'shape': ['02', '12', '01', '11']},
        'I': {'color': 'palegreen', 'shape': ['00', '01', '02', '03']},
        'J': {'color': 'coral', 'shape': ['01', '11', '21', '22']},
        'L': {'color': 'red2', 'shape': ['21', '11', '01', '00']},
        'T': {'color': 'gold', 'shape': ['11', '01', '21', '10']},
        'Z': {'color': 'Lightskyblue', 'shape': ['01', '11', '10', '20']},
        'S': {'color': 'hotpink1', 'shape': ['10', '11', '01', '02']},
        'E': {'color': 'orchid1', 'shape': ['00', '01', '02', '10']},
        'G': {'color': 'brown1', 'shape': ['01', '11', '21', '02']},
        'I_vert': {'color': 'cornflowerblue', 'shape': ['00', '10', '20', '30']},
        'T_right': {'color': 'seagreen1', 'shape': ['10', '11', '12', '01']},
        'T_vnis': {'color': 'mediumpurple1', 'shape': ['01', '11', '21', '12']}
    }

    def __init__(self, type=None):
        if type is None:
            self.type = random.choice(list(self.figures.keys()))
        else:
            self.type = type
        self.color = self.figures[self.type]['color']
        self.shape = self.figures[self.type]['shape']

    def get_shape_positions(self, x, y):
        """Calculate the absolute board positions of the figure based on top-left corner (x, y)."""
        return [(x + int(pos[0]), y + int(pos[1])) for pos in self.shape]
