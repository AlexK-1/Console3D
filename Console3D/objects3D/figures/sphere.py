from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Sphere(BaseFigure):
    """Объект сферы."""
    def __init__(self,
                 position: Sequence[Union[int, float]],
                 diameter: Union[int, float],
                 reflects: Union[int, float] = 0,
                 visible: bool = True
                ) -> NoReturn:
        """
        Создание объекта сферы.
        :param position: координаты центра сфера
        :param diameter: диаметр сферы
        :param reflects: способность объекта отражать другие объекты (работать как зеркало)
        :param visible: будет ли отрисовываться эта сфера
        """
        super().__init__(position, [1.0, 0.0, 0.0], diameter, reflects, visible)
    
    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """Функция пересечения луча со сферой"""
        b = 2 * np.dot(rd, np.array(ro) - np.array(self.pos))
        c = np.linalg.norm(np.array(ro) - np.array(self.pos)) ** 2 - self.size ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                intersection_pos = np.array(np.array(ro) + np.array(rd) * min(t1, t2))
                return True, min(t1, t2), self.normal_dir(intersection_pos)
        return False, -1.0, [0.0, 0.0, 0.0]
    
    def normal_dir(self, intersection_pos: Sequence[float]) -> Sequence[float]:
        return normalize(intersection_pos - np.array(self.pos))