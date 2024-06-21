from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np


from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Box(BaseFigure):
    """The object of a rectangular parallelepiped."""
    def __init__(self,
                 position: Sequence[Union[int, float]],
                 direction: Sequence[float],
                 size: Sequence[Union[int, float]],
                 reflects: Union[float, int] = 0,
                 visible: bool = True
                ) -> NoReturn:
        """
        Creating a rectangular parallelepiped object.
        :param position: coordinates of the center
        :param direction: the direction vector of one of the faces
        :param size: the size of the parallelepiped along three axes
        :param reflects: the ability of an object to reflect other objects (work as a mirror)
        :param visible: will this figure be rendered
        """
        super().__init__(position, direction, size, reflects, visible)

    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """Функция пересечения луча с прямоугольным параллелепипедом"""

        def kostyl(x: int):  # костыль, убирающий полоску с куба
            if x == 0:
                return 50
            else:
                return 1/x
        new_ro = ro - self.pos
        m = np.array(list(map(kostyl, rd)))
        n = m * new_ro
        k = abs(m) * self.size
        t1 = -n - k
        t2 = -n + k
        tn = max(t1[0], t1[1], t1[2])
        tf = min(t2[0], t2[1], t2[2])
        if tn > tf or tf < 0:
            return False, -1.0, [0.0, 0.0, 0.0]
        yzx = [t1[1], t1[2], t1[0]]
        zxy = [t1[2], t1[0], t1[1]]
        out_normal = -np.array(sign(rd)) * step(yzx, t1) * step(zxy, t1)
        return True, min(tn, tf), out_normal
