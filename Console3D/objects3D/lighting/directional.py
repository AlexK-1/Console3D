from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional, List
import math
import numpy as np

from .base import BaseLight


class DirectionalLight(BaseLight):
    """
    Направленный источник света. Не имеет положения, есть только направление.
    Светит только в одну сторону. Является аналогом солнечного освещения.
    """
    def __init__(self, direction: Sequence[float], power: Union[int, float]) -> NoReturn:
        """
        Создание направленного источника освещения.
        :param direction: направление источника света
        :param power: сила источника света от 0 до 1
        """
        super().__init__([0, 0, 0], direction, power)
    
    def get_dir(self, *args: Any, **kwargs: Any) -> np.ndarray:
        return self.dir
    
    def get_distance(self, position) -> float:
        return math.inf