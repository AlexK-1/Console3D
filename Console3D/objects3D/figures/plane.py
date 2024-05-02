from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Plane(BaseFigure):
    """Объект плоскости. Плоскость имеет только позицию z. Плоскость бесконечна"""
    def __init__(self, position: Sequence[Union[int, float]], direction: Sequence[float], reflects: Union[int, float] = 0, visible: bool = True) -> NoReturn:
        """
        Создание объекта плоскости.
        :param position: координата точки на плоскости
        :param direction: направление нормали плоскости
        :param reflects: способность объекта отражать другие объекты (работать как зеркало)
        :param visible: будет ли отрисовываться эта фигура
        """
        super().__init__(position, direction, 1.0, reflects, visible)
    
    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """Функция пересечения луча с плоскостью."""
        denominator = np.dot(rd, self.dir)
    
        if np.abs(denominator) < 1e-6:
            return False, -1.0, [0.0, 0.0, 0.0]
        
        t = np.dot(np.array(self.pos) - ro, self.dir) / denominator
        
        if t < 0:
            return False, -1.0, [0.0, 0.0, 0.0]
        
        return True, t, self.dir
