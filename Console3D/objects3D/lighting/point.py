from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math

from .base import BaseLight
from ...vec_functions import *


class PointLight(BaseLight):
    """Класс точечного источника освещения. Светит во все стороны сразу и имеет позицию."""
    def __init__(self, position: Sequence[Union[float, int]], power: Union[int, float]) -> NoReturn:
        """
        Создание точечного источника света.
        :param position: позиция точечного источника
        :param power: сила источника света от 0 до 1
        """
        super().__init__(position, [0.0, 0.0, -1.0], power)
    
    def get_dir(self, position) -> Sequence[float]:
        """Направление высчитывается относительно определённых координат (position),
        т.к. источник светит во все стороны"""
        return normalize(position - np.array(self.pos))
    
    def get_distance(self, position) -> float:
        return vector_length(np.array(position) - self.pos)