from .point import Point
from .onshowobject import OnShowObject


class Player(OnShowObject):
    def __init__(self, pos: Point, name: str = ''):
        """
        初始化一个玩家
        :param pos: 初始位置
        :param name: 名字（其实没用）
        """
        super().__init__()
        self.pos = pos
        self.name = name
        self.step = 0
        """移动步数"""
        self.move_times = 0
        """移动次数"""
