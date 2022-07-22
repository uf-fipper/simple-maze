import os

from maze import *
from .exceptions import *

# from pynput.keyboard import on_press, KeyboardEvent

from typing import Iterable, Union, Optional, Callable
from pynput import keyboard
from pynput.keyboard import KeyCode, Key, HotKey
from threading import Lock

_T_KC = Optional[Union[Key, KeyCode]]


class Play:
    @property
    def how_to_play(self):
        return (
            f"游戏可能会莫名其妙闪退，不要在意这些细节\n"
            f"玩法：方向键移动，会自动寻找下一个分叉点，会记录当前步数\n"
            f"起点保证在左上角，终点保证在右下角\n"
            f"'R': 人物会回到起点\n"
            f"'ctrl + R': 重新开始，人物会回到起点\n"
            f"'ctrl + S': 求解，显示当前位置到终点的路径，再按一次取消\n"
            # f"'ctrl + N': 生成同长同宽的新地图\n"
            # f"'ctrl + M': 新地图，重新输入长和宽\n"
            # f"'ctrl + X': 结束游戏\n"
        )

    def __init__(self):
        self.game = Game(2, 2)
        self.container: Optional[OnShowContainer] = None
        self.game_show: Optional[GameShow] = None
        self.tips = ''
        self.listener: Optional[keyboard.Listener] = None
        self.listener_over = False
        
        self.attr_lock = Lock()
        self._is_restart = False
        self._is_solve = False
        
    @property
    def is_restart(self):
        with self.attr_lock:
            return self._is_restart

    @is_restart.setter
    def is_restart(self, value):
        with self.attr_lock:
            self._is_restart = value
            
    @property
    def is_solve(self):
        with self.attr_lock:
            return self._is_solve

    @is_solve.setter
    def is_solve(self, value):
        with self.attr_lock:
            self._is_solve = value

    def run(self):
        while True:
            if self.is_restart:
                self.game = Game(self.game.row, self.game.column, random=Random(self.game.random.raw_seed))
                self.is_restart = False
            else:
                self.new_game()
            while True:
                self.game_show = StrGameShow(self.game, self.container)

                if self.game.is_win:
                    # self.tips = "恭喜你获得胜利！按 ctrl + 'N' 或 ctrl + 'M' 开始新游戏"
                    print('恭喜你获得胜利！')
                    print(self.game_show.format())
                    # os.system("pause")
                    input('按下回车结束游戏：')
                    return
                else:
                    self.tips = ""
                self.show()
                self.listen()
                # os.system('cls')
                
                if self.is_restart:
                    break

    def show(self):
        if not self.game_show:
            raise Exception
        print(self.how_to_play)
        print(f'种子：{self.game.map.random.raw_seed}')
        print(f'步数：{self.game.player.step}')
        print(f'执行次数：{self.game.player.move_times}')
        
        self.game_show.update()
        if self.is_solve and not self.game.is_win:
            solve_list = self.game.solve()
            for l in solve_list[1:-1]:
                self.game_show[l] = self.game_show.container[GameValue.solve]
        
        print(self.game_show.format())
        print(self.tips)

    def on_press(self, key: _T_KC):
        if key is None:
            return
        if self.listener_over:
            return
        
        key_actions: dict[_T_KC, Callable[[], None]] = {
            Key.up: lambda: self.game.move(MoveStatus.up),
            Key.down: lambda: self.game.move(MoveStatus.down),
            Key.left: lambda: self.game.move(MoveStatus.left),
            Key.right: lambda: self.game.move(MoveStatus.right),
            KeyCode(char='r'): lambda: self.game.move_player(self.game.map.st),
            KeyCode(char='R'): lambda: self.game.move_player(self.game.map.st),
            KeyCode(char='\x12'): lambda: setattr(self, 'is_restart', True),
        }
        if key in key_actions:
            key_actions[key]()
        elif key == KeyCode(char='\x12'):  # ctrl + R
            self.is_restart = True
        elif key == KeyCode(char='\x13'):  # ctrl + S
            with self.attr_lock:
                self._is_solve = not self._is_solve
        else:
            return
        self.listener_over = True

    def listen(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        while not self.listener_over:
            pass
        self.listener.stop()
        self.listener_over = False

    def new_game(self) -> Game:
        while True:
            inps = input('请输入迷宫的行和列，中间用空格隔开：').split()
            try:
                args = map(lambda x: int(x), inps)
                break
            except ValueError:
                print('确保输入是两个整数，', end='')
        self.game = Game(*args)
        return self.game
