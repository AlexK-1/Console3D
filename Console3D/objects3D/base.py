from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence

from ..vec_functions import *


class BaseObject3D(ABC):
    """
    Базовый класс 3D объекта (фигура, источник света и т.д.)
    """
    def __init__(self, position: Sequence[Union[float, int]], direction: Sequence[float]) -> NoReturn:
        """
        Создание 3D объекта
        :param position: позиция объекта
        :param direction: направление объекта
        """
        self.pos = list(position)
        self.dir = normalize(direction)
    
    def move_to(self, position: Sequence[Union[float, int]]) -> Sequence[Union[float, int]]:
        """
        Перемещает объект в заданные координаты
        :param position: новые координаты объекта
        :return: новые координаты объекта
        """
        self.pos = position
        return self.pos

    def rotate_to(self, direction: Sequence[float]) -> Sequence[float]:
        """
        Устанавливает направление объекта
        :param direction: вектор нового направления объекта
        :return: вектор нового направления объекта
        """
        self.dir = normalize(direction)
        return self.dir
    
    def rotate_x(self, degree: Union[int, float]) -> Sequence[float]:
        """
        Поворачивает объект вокруг оси x на определённый градус
        :param degree: градус, на который поворачивается объект
        :return: вектор нового направления объекта
        """
        self.dir = rotate_vector_x(self.dir, degree)
        return self.dir
    
    def rotate_y(self, degree: Union[int, float]) -> Sequence[float]:
        """
        Поворачивает объект вокруг оси y на определённый градус
        :param degree: градус, на который поворачивается объект
        :return: вектор нового направления объекта
        """
        self.dir = rotate_vector_y(self.dir, degree)
        return self.dir

    def rotate_z(self, degree: Union[int, float]) -> Sequence[float]:
        """
        Поворачивает объект вокруг оси z на определённый градус
        :param degree: градус, на который поворачивается объект
        :return: вектор нового направления объекта
        """
        self.dir = rotate_vector_z(self.dir, degree)
        return self.dir
