import enum


class MapValue(enum.Enum):
    empty = '?'
    wall = 'O'
    road = ' '
    border = 'X'
    move = '.'
    st = 'P'
    ed = 'E'
