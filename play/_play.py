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
        self._is_restart = False
        self._is_solve = False
            
    def restart(self):
        self.game = Game(self.game.row, self.game.column, random=Random(self.game.random.raw_seed))
        self._is_restart = False

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
                if self._is_restart:
                    self.restart()
                else:
                    self.new_game()
                self.new_game_show()
                while True:
                    self.show()
                    self.wait_action()
                    
                    if self._is_restart:
                        break
        except StopException:
            return
