from random import Random
from time import time_ns

from typing import List


class Random(Random):  # type: ignore
    def __init__(self, x=None):
        if x is None:
            x = time_ns()
        super().__init__(x)
        self.raw_seed = x

    def randindex(self, n: int):
        if n <= 0:
            raise ValueError('长度必须小于0')
        res = [i for i in range(n)]
        for i in range(n):
            temp = self.randint(i, n - 1)
            res[i], res[temp] = res[temp], res[i]
        return res

    def randarray(self, arr: list):
        res_index = self.randindex(len(arr))
        res: list = [None] * len(arr)
        for i, index in enumerate(res_index):
            res[i] = arr[index]
        return res
