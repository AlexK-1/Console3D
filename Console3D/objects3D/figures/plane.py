from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Plane(BaseFigure):
    """An object of an infinite plane"""
    def __init__(self, position: Sequence[Union[int, float]], direction: Sequence[float], reflects: Union[int, float] = 0, visible: bool = True):
        """
        Creating a plane object.
        :param position: the coordinate of a point on the plane
        :param direction: the direction of the plane normal
        :param reflects: the ability of an object to reflect other objects (work as a mirror)
        :param visible: will this figure be rendered
        """
        super().__init__(position, normalize(direction), 1.0, reflects, visible)

    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """Функция пересечения луча с плоскостью."""
        denominator = np.dot(rd, self.dir)
    
        if np.abs(denominator) < 1e-6:
            return False, -1.0, [0.0, 0.0, 0.0]
        
        t = np.dot(self.pos - ro, self.dir) / denominator
        
        if t < 0:
            return False, -1.0, [0.0, 0.0, 0.0]
        
        return True, t, self.dir
