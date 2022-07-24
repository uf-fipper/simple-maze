from manimlib import *

from maze import *
from .exceptions import *

from typing import Iterable, Union, Optional, Callable


class AbstractPlay:
    def __init__(self):
        self.game: Game
        self.game_show: GameShow
        self.tips = ''
        
        self.last_action = None
        self._is_solve = False
            
    def restart(self):
        self.game.restart()
        self.new_game_show()

    def new_game(self) -> Game:
        raise NotImplementedError
        
    def new_game_show(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError
    
    def wait_action(self):
        raise NotImplementedError

    def run(self):
        try:
            while True:
                self.new_game()
                self.new_game_show()
                while True:
                    self.show()
                    self.wait_action()
        except StopException:
            return
