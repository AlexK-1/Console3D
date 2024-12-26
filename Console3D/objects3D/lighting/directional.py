from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional, List
import math
import numpy as np

from .base import BaseLight


class DirectionalLight(BaseLight):
    """
    A directional light source. It has no position, there is only a direction.
    It shines only in one direction. It is an analogue of solar lighting.
    """
    def __init__(self, direction: Sequence[float], power: Union[int, float]):
        """
        Creating a directional lighting source.
        :param direction: the direction of the light source
        :param power: light source power from 0 to 1
        """
        super().__init__([0, 0, 0], direction, power)
    
    def get_dir(self, *args: Any, **kwargs: Any) -> np.ndarray:
        return self.dir
    
    def get_distance(self, position) -> float:
        return math.inf