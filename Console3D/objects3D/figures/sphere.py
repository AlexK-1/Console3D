from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Sphere(BaseFigure):
    """The object of the sphere."""
    def __init__(self,
                 position: Sequence[Union[int, float]],
                 diameter: Union[int, float],
                 reflects: Union[int, float] = 0,
                 visible: bool = True
                ):
        """
        Creating a sphere object.
        :param position: coordinates of the center of the sphere
        :param diameter: diameter of the sphere
        :param reflects: the ability of an object to reflect other objects (work as a mirror)
        :param visible: will this sphere be rendered
        """
        super().__init__(position, [1.0, 0.0, 0.0], diameter, reflects, visible)
        self.cache_size_squared = None
        self.cache_size_squared_pr = 0

    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """Функция пересечения луча со сферой"""
        b = 2 * np.dot(rd, ro - self.pos)
        if not self.cache_size_squared or self.cache_size_squared_pr != self.size:
            self.cache_size_squared = self.size ** 2
            self.cache_size_squared_pr = self.size
        c = np.linalg.norm(ro - self.pos) ** 2 - self.cache_size_squared
        delta = b ** 2 - 4 * c
        if delta > 0:
            t1 = (-b + np.sqrt(delta)) / 2
            t2 = (-b - np.sqrt(delta)) / 2
            if t1 > 0 and t2 > 0:
                intersection_pos = ro + np.array(rd) * min(t1, t2)
                return True, min(t1, t2), self.normal_dir(intersection_pos)
        return False, -1.0, [0.0, 0.0, 0.0]
    
    def normal_dir(self, intersection_pos: Sequence[float]) -> Sequence[float]:
        return normalize(intersection_pos - self.pos)