from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseLight
from ...vec_functions import *


class PointLight(BaseLight):
    """The class of the point light source. It shines in all directions at once and has a position."""
    def __init__(self, position: Sequence[Union[float, int]], power: Union[int, float]):
        """
        Creating a point light source.
        :param position: position of the point source
        :param power: light source power from 0 to 1
        """
        super().__init__(position, [0.0, 0.0, -1.0], power)
    
    def get_dir(self, position) -> np.ndarray:
        """Направление высчитывается относительно определённых координат (position),
        т.к. источник светит во все стороны"""
        return normalize(position - np.array(self.pos))
    
    def get_distance(self, position) -> float:
        return vector_length(np.array(position) - self.pos)