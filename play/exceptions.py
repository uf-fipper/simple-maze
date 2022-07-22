from maze.exceptions import *


class PlayException(MazeException):
    pass


class RestartException(PlayException):
    pass


class StopException(PlayException):
    pass
