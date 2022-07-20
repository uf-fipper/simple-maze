from collections import namedtuple


class Point(namedtuple('Point', 'x y')):
    def get_range(self):
        return [
            Point(self[0] - 1, self[1]),
            Point(self[0] + 1, self[1]),
            Point(self[0], self[1] - 1),
            Point(self[0], self[1] + 1),
        ]
