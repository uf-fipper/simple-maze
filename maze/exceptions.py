class MazeException(Exception):
    pass


class MapInitException(MazeException):
    pass


class SolveException(MazeException):
    pass


class QueueEmptyException(MazeException):
    pass
