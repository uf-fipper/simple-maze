from manimlib import *
from pyglet.window import key

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
                Text('.', height=self.side_length / 4, width=self.side_length / 4),
            )
            return obj

        @self(GameValue.solve)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('+', height=self.side_length / 2, width=self.side_length / 2),
            )
            return obj

        @self(MapValue.st)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('始', font="宋体", height=self.side_length, width=self.side_length)
            )
            return obj

        @self(MapValue.ed)
        def _(x):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('终', font="宋体", height=self.side_length, width=self.side_length)
            )
            return obj

        @self(Player)
        def _(x: Player):
            obj = VGroup(
                Square(self.side_length).set_stroke(opacity=0),
                Text('人', font="宋体", height=self.side_length, width=self.side_length)
            )
            return obj


class ManimglGameShow(GameShow[Mobject]):
    def __init__(self, game: Game):
        if (game.column + 2) / (game.row + 2) >= ASPECT_RATIO:
            side_length = FRAME_WIDTH / (game.column + 2)
        else:
            side_length = FRAME_HEIGHT / (game.row + 2)
        super().__init__(game, ManimContainer(side_length), dtype=object)

    def format(self) -> Group:
        group = Group()
        for row in self._result:
            for obj in row:
                group.add(obj)
        return group.arrange_in_grid(*self._result.shape, buff=0)
    
    
class GameTextbox(Textbox):
    def on_key_press(self, mob: Mobject, event_data: dict[str, int]) -> Optional[bool]:
        symbol = event_data['symbol']
        modifiers = event_data['modifiers']
        modifiers = modifiers & ~key.MOD_NUMLOCK  # 排除小键盘NumLock
        modifiers = modifiers & ~key.MOD_CAPSLOCK  # 排除CapsLK
        print(symbol, modifiers)
        if modifiers:
            return None
        if symbol == key.BACKSPACE:  # backspace
            return super().on_key_press(mob, {'symbol': symbol, 'modifiers': modifiers})
        if len(self.text.text) >= 2:
            return None
        if key.NUM_0 <= symbol <= key.NUM_9:
            symbol -= (key.NUM_0 - key._0)
        if key._0 <= symbol <= key._9:
            return super().on_key_press(mob, {'symbol': symbol, 'modifiers': modifiers})
        return None


class Play(Scene, AbstractPlay):
    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)
        AbstractPlay.__init__(self)
        self.start_next = True
        self.confirm_mutex = False
        self.show_group: Optional[Group] = None
        self.input_group: Optional[Group] = None

    def new_game(self):
        if self.show_group:
            self.play(FadeOut(self.show_group))
            self.show_group = None
            
        def confirm_on_click(mob: Mobject):
            try:
                if self.confirm_mutex:
                    return
                self.confirm_mutex = True
                row = int(row_label.text.text)
                column = int(column_label.text.text)
                if row < 2 or column < 2:
                    raise ValueError
                self.game = Game(row, column)
                self.new_game_show()
                self.show()
            except ValueError:
                assert self.input_group is not None
                input_group2 = Group(*self.input_group[:-1], Text("行和列都必须是大于1的整数", font="宋体")).arrange(DOWN)
                self.remove(self.input_group)
                self.add(input_group2)
                self.input_group = input_group2
            finally:
                self.confirm_mutex = False
            
        row_label = GameTextbox("7")
        column_label = GameTextbox("14")
        confirm_button = Button(Square(), on_click=confirm_on_click)
        tips = Text("", font="宋体")
        self.input_group = Group(row_label, column_label, confirm_button, tips).arrange(DOWN)
        self.add(self.input_group)

    def new_game_show(self):
        self.game_show = ManimglGameShow(self.game)

    def show(self):
        if self.input_group:
            self.remove(self.input_group)
            self.input_group = None
        self.game_show.update()
        group = self.game_show.format()
        if self.show_group is None:
            self.play(ShowCreation(group))
            self.show_group = group
        else:
            self.play(Transform(self.show_group, group))
        if self.game.is_win:
            self.new_game()
            return
        self.start_next = False

    def wait_action(self):
        self.wait(10086, lambda: self.start_next, note="等待操作...")
    
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.start_next:
            return super().on_key_press(symbol, modifiers)
        self.start_next = True
        try:
            char = chr(symbol)
        except OverflowError:
            log.warning("The value of the pressed key is too large.")
            return
        modifiers = modifiers & ~key.MOD_NUMLOCK  # 排除小键盘NumLock
        modifiers = modifiers & ~key.MOD_CAPSLOCK  # 排除CapsLK
        if not modifiers:
            # 没有功能键
            if symbol == key.LEFT:  # 左
                self.game.move(MoveStatus.left)
            elif symbol == key.UP:  # 上
                self.game.move(MoveStatus.up)
            elif symbol == key.RIGHT:  # 右
                self.game.move(MoveStatus.right)
            elif symbol == key.DOWN:  # 下
                self.game.move(MoveStatus.down)
            else:
                return super().on_key_press(symbol, modifiers)
            self.show()
        
        elif modifiers == key.MOD_CTRL:
            if symbol == key.R:
                self.restart()
            else:
                return super().on_key_press(symbol, modifiers)
            self.show()
            
        else:
            return super().on_key_press(symbol, modifiers)

    def setup(self) -> None:
        self.new_game()
