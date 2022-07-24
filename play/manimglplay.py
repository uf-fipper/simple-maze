from manimlib import *

from maze import *
from .exceptions import *
from ._play import AbstractPlay

from typing import Iterable, Union, Optional, Callable


class ManimContainer(OnShowContainer[Mobject]):
    def __init__(self, side_length: int):
        super().__init__()
        self.side_length = side_length
        self._init()
        
    def _init(self):
        @self(MapValue.border)
        def _(x):
            obj = Square(self.side_length)
            obj.set_color(RED)
            return obj
            
        @self(MapValue.wall)
        def _(x):
            obj = Square(self.side_length)
            obj.set_color(YELLOW)
            return obj
        
        @self(MapValue.road)
        def _(x):
            obj = Square(self.side_length)
            return obj
        
        @self(GameValue.move)
        def _(x):
            obj = VGroup(
                Square(self.side_length),
                Text('.'),
            )
            return obj
        
        @self(GameValue.solve)
        def _(x):
            obj = VGroup(
                Square(self.side_length),
                Text('+'),
            )
            return obj
            
        @self(MapValue.st)
        def _(x):
            obj = VGroup(
                Square(self.side_length),
                Text('S')
            )
            return obj
        
        @self(MapValue.ed)
        def _(x):
            obj = VGroup(
                Square(self.side_length),
                Text('E')
            )
            return obj
        
        @self(Player)
        def _(x: Player):
            obj = VGroup(
                Square(self.side_length),
                Text('P')
            )
            return obj


class ManimglGameShow(GameShow[Mobject]):
    def __init__(self, game: Game):
        super().__init__(game, ManimContainer(2), dtype=object)
        
    def format(self) -> Group:
        group = Group(*(obj for obj in (objs for objs in self._result)))


class ColorStrGameShow(GameShow[Mobject]):
    def __init__(self, game: Game):
        super().__init__(game, ManimContainer(2), dtype=object)

    def format(self) -> Group:
        group = Group()
        for row in self._result:
            for obj in row:
                group.add(obj)
        return group.arrange_in_grid(*self._result.shape)


class Play(Scene, AbstractPlay):
    def __init__(self):
        Scene.__init__(self)
        AbstractPlay.__init__(self)

    def new_game(self) -> Game:
        self.game = Game(5, 7)
        return self.game
        
    def new_game_show(self):
        self.game_show = ManimglGameShow(self.game)

    def show(self):
        group = self.game_show.format()
        self.play(Write(group))
    
    def wait_action(self):
        pass
    
    def construct(self) -> None:
        self.run()
