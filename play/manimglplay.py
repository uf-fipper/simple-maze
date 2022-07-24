from manimlib import *

from maze import *
from .exceptions import *
from ._play import AbstractPlay

import logging

from typing import Iterable, Union, Optional, Callable

log = logging.getLogger("manimgl")


class ManimContainer(OnShowContainer[Mobject]):
    def __init__(self, side_length: int):
        super().__init__()
        self.side_length = side_length
        self._init()

    def _init(self):
        @self(MapValue.border)
        def _(x):
            obj = Square(self.side_length)
            obj.set_stroke(opacity=0)
            obj.set_fill(color=RED, opacity=1)
            return obj

        @self(MapValue.wall)
        def _(x):
            obj = Square(self.side_length)
            obj.set_stroke(opacity=0)
            obj.set_fill(color=YELLOW, opacity=1)
            return obj

        @self(MapValue.road)
        def _(x):
            obj = Square(self.side_length)
            obj.set_stroke(opacity=0)
            return obj

        @self(GameValue.move)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('.'),
            )
            return obj

        @self(GameValue.solve)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('+'),
            )
            return obj

        @self(MapValue.st)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('始', font="微软雅黑")
            )
            return obj

        @self(MapValue.ed)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('终', font="微软雅黑")
            )
            return obj

        @self(Player)
        def _(x: Player):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('人', font="微软雅黑")
            )
            return obj


class ManimglGameShow(GameShow[Mobject]):
    def __init__(self, game: Game):
        super().__init__(game, ManimContainer(1), dtype=object)

    def format(self) -> Group:
        group = Group()
        for row in self._result:
            for obj in row:
                group.add(obj)
        return group.arrange_in_grid(*self._result.shape, buff=0)


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
    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)
        AbstractPlay.__init__(self)
        self.start_next = True
        self.show_group: Optional[Group] = None

    def new_game(self) -> Game:
        self.game = Game(4, 8, random=Random(123456))
        return self.game

    def new_game_show(self):
        self.game_show = ManimglGameShow(self.game)

    def show(self):
        self.game_show.update()
        group = self.game_show.format()
        if self.show_group is None:
            self.play(ShowCreation(group))
            self.show_group = group
        else:
            self.play(Transform(self.show_group, group))
        if self.game.is_win:
            raise StopException
        self.start_next = False

    def wait_action(self):
        self.wait(10086, lambda: self.start_next, note="等待操作...")
    
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.start_next:
            return super().on_key_press(symbol, modifiers)
        try:
            char = chr(symbol)
        except OverflowError:
            log.warning("The value of the pressed key is too large.")
            return
        if modifiers == 16:
            # 没有功能键
            if symbol == 65361:  # 左
                self.game.move(MoveStatus.left)
            elif symbol == 65362:  # 上
                self.game.move(MoveStatus.up)
            elif symbol == 65363:  # 右
                self.game.move(MoveStatus.right)
            elif symbol == 65364:  # 下
                self.game.move(MoveStatus.down)
            else:
                return super().on_key_press(symbol, modifiers)
            self.start_next = True
        
        elif modifiers == 18:  # ctrl
            if char == 'r':
                self.restart()
            else:
                return super().on_key_press(symbol, modifiers)
            self.start_next = True
            
        else:
            return super().on_key_press(symbol, modifiers)

    def construct(self) -> None:
        AbstractPlay.run(self)
