class MazeException(Exception):
    pass


class MapException(MazeException):
    pass


class MapInitException(MapException):
    pass


class MapIndexError(MapException, IndexError):
    pass


class GameException(MazeException):
    pass


class GameMoveException(GameException):
    pass


class SolveException(MazeException):
    pass


class QueueEmptyException(MazeException):
    pass
