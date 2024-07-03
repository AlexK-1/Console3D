from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence

from ..vec_functions import *
from .base import BaseObject3D
from .objs_list import camera_object
from . import objs_list


class Camera(BaseObject3D):
    """The class of the camera that the user will see from."""

    def __init__(self, position: Sequence[Union[float, int]], direction: Sequence[float]) -> NoReturn:
        """
        Creating a camera object. There can only be one camera object on the scene.
        :param position: camera coordinates
        :param direction: the direction of the camera as a vector
        """
        global camera_object

        super().__init__(position, direction)
        objs_list.camera_object = self
