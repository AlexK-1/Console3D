from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Box(BaseFigure):
    """Объект прямоугольного параллелепипеда."""
    def __init__(self,
                 position: Sequence[Union[int, float]],
                 direction: Sequence[float],
                 size: Sequence[Union[int, float]],
                 reflects: Union[float, int] = 0,
                 visible: bool = True
                ) -> NoReturn:
        """
        Создание объекта прямоугольного параллелепипеда.
        :param position: координаты центра
        :param direction: вектор направления одной из граней
        :param size: размер параллелепипеда по трём осям
        :param reflects: способность объекта отражать другие объекты (работать как зеркало)
        :param visible: будет ли отрисовываться эта фигура
        """
        super().__init__(position, direction, size, reflects, visible)
    
    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """Функция пересечения луча с прямоугольным параллелепипедом"""
        if 0 in rd:
            m = []
            for d in rd:
                if d != 0:
                    m.append(1/d)
                else:
                    m.append(50)  # небольшой костыль, который убирает чёрную полоску с куба
            m = np.array(m)
        else:
            m = np.ones(3) / np.array(rd)
        # print(m)
        n = m * (np.array(ro) - np.array(self.pos))
        k = abs(m) * np.array(self.size)
        t1 = -n - k
        t2 = -n + k
        tn = max(max(t1[0], t1[1]), t1[2])
        tf = min(min(t2[0], t2[1]), t2[2])
        if tn > tf or tf < 0:
            return False, -1.0, [0.0, 0.0, 0.0]
        yzx = [t1[1], t1[2], t1[0]]
        zxy = [t1[2], t1[0], t1[1]]
        out_normal = -np.array(sign(rd)) * np.array(step(yzx, t1)) * np.array(step(zxy, t1))
        return True, min(tn, tf), out_normal
