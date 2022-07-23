import enum


class MapValue(enum.Enum):
    empty = '?'
    wall = 'O'
    road = ' '
    border = 'X'
    st = 'P'
    ed = 'E'
