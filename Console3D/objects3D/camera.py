from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence

from ..vec_functions import *
from .base import BaseObject3D
from .objs_list import camera_object
from . import objs_list


class Camera(BaseObject3D):
    """Класс камеры, из которой будет видеть пользователь."""

    def __init__(self, position: Sequence[Union[float, int]], direction: Sequence[float]) -> NoReturn:
        """
        Создание объекта камеры. На сцене может быть только один объект камеры.
        """
        global camera_object

        super().__init__(position, direction)
        objs_list.camera_object = self
