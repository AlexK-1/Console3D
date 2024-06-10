from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from ..base import BaseObject3D
from ..objs_list import light_objects, figures_objects


class BaseLight(BaseObject3D):
    """
    Базовый объект освещения.
    """
    def __init__(self,
                 position: Sequence[Union[float, int]],
                 direction: Sequence[float],
                 power: Union[int, float],
                 *args: Any, **kwargs: Any
                ) -> NoReturn:
        """
        Создание источника освещения
        :param position: позиция источника света
        :param direction: направление источника света
        :param power: сила источника света от 0 до 1
        """
        global light_objects
        super().__init__(position, direction)
        self.power = power
        light_objects.append(self)  # добавление источника освещения в список
    
    def get_dir(self, *args: Any, **kwargs: Any) -> Sequence[float]:
        """
        Возвращает направление света (может быть, например, светить всегда в одну сторону или во все стороны)
        """
        pass

    def get_distance(self, position) -> float:
        """
        Определяет расстояние от источника света до определённой точки
        :param position: позиция точки, до которого нужно узнать расстояние
        :return: расстояние от источника света до точки
        """
        pass
