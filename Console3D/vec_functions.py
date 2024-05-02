import numpy as np
import math
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence


def vector_length(vector: Sequence[float]) -> float:
    """Определяет длину вектора по теореме Пифагора"""
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def normalize(vector: Sequence[float]) -> Sequence[float]:
    """Нормализация вектора"""
    length = vector_length(vector)
    return [vector[0]/length, vector[1]/length, vector[2]/length]

def sign(value: Union[Sequence[Union[float, int]], float, int]) -> int:
    """Определяет знак числа или всех чисел в списке
    :return 0 если 0, -1 если отрицательное, 1 если положительное"""
    if type(value) == list or type(value) == np.ndarray:
        a = []
        for i in list(value):
            # print(i, value)
            a.append((0 < float(i)) - (float(i) < 0))
        return a
    return (0 < value) - (value < 0)

def step(edge: Sequence[Union[float, int]], x: Sequence[Union[float, int]]) -> Sequence[int]:
    """Определяет, больше значения списка x соответствующих значений списка edge
    :return Список чисел (0 если меньше или равно, 1 если больше)"""
    a = []
    for i in range(len(edge)):
        a.append(int(x[i] > edge[i]))
    return a

def rotate_vector_x(vector: Sequence[float], degree: Union[float, int]) -> Sequence[float]:
    new_y = vector[1] * math.cos(math.radians(degree)) - vector[2] * math.sin(math.radians(degree))
    new_z = vector[1] * math.sin(math.radians(degree)) + vector[2] * math.cos(math.radians(degree))
    return [vector[0], new_y, new_z]

def rotate_vector_y(vector: Sequence[float], degree: Union[float, int]) -> Sequence[float]:
    new_x = vector[0] * math.cos(math.radians(degree)) - vector[2] * math.sin(math.radians(degree))
    new_z = vector[0] * math.sin(math.radians(degree)) + vector[2] * math.cos(math.radians(degree))
    return [new_x, vector[1], new_z]

def rotate_vector_z(vector: Sequence[float], degree: Union[float, int]) -> Sequence[float]:
    new_x = vector[0] * math.cos(math.radians(degree)) - vector[1] * math.sin(math.radians(degree))
    new_y = vector[0] * math.sin(math.radians(degree)) + vector[1] * math.cos(math.radians(degree))
    return [new_x, new_y, vector[2]]

def reflect(vector: Sequence[float], normal: Sequence[float]):
    """Отражает вектор относительно нормали поверхности"""
    return np.array(vector) - 2 * np.dot(normal, vector) * np.array(normal)
