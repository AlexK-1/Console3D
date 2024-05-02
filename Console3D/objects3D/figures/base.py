from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence
import numpy as np
import math

from ..base import BaseObject3D
from ..objs_list import light_objects, figures_objects
from ..lighting.base import BaseLight
from ...utils import *


class BaseFigure(BaseObject3D):
    """
    Базовый класс для 3D фигур
    """
    def __init__(self,
                 position: Sequence[Union[int, float]],
                 direction: Sequence[float],
                 size: Union[int, float, Sequence[Union[int, float]]],
                 reflects: Union[float, int] = 0,
                 visible: bool = True
                ) -> NoReturn:
        """
        Создание фигуры.
        :param position: позиция центра фигуры
        :param direction: направление объекта
        :param size: размер объекта, может быть одно число, как у сферы, или список, как у куба
        :param reflects: способность объекта отражать другие объекты (работать как зеркало)
        :param visible: будет ли отрисовываться этот объект
        """
        super().__init__(position, direction)
        self.size = size
        self.visible = visible
        self.reflects = reflects
        figures_objects.append(self)
    
    def intersect(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """
        Проверка на наличие пересечений луча с объектом (если visible == False, функция должна возвращать False)
        :param ro: координаты начала луча
        :param rd: вектор направления луча
        :return: наличие пересечения, расстояние до точки пересечения, направление нормали
        """
        if not self.visible:
            return False, -1.0, [0.0, 0.0, 0.0]
        return self.ray_intersection_fn(ro, rd)
    
    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """
        Функция пересечения луча с фигурой. В классе фигуры должна быть перезаписана.
        :param ro: координаты начала луча
        :param rd: вектор направления луча
        :return: наличие пересечения, расстояние до точки пересечения, направление нормали
        """
        pass
    
    def normal_dir(self, intersection_pos: Sequence[float]) -> Sequence[float]:
        """
        Определение нормали в точке на объекте. Необязательная функция для объекта.
        :param intersection_pos: координата точки пересечения
        :return: вектор направления нормали объекта
        """
        return [0, 0, 0]
    
    def lightning(self, normal_dir: Sequence[float], intersection_pos: Sequence[Union[int, float]]) -> float:
        """
        Определяет освещённость точки на объекте. Подразумевается, что пересечение объекта с лучом есть.
        :param normal_dir: вектор направления нормали
        :param intersection_pos: координаты точки пересечения луча с объектом
        :return: освещённость точки от 0 до 1
        """
        if len(light_objects) == 0:
            return 0
        
        light = 0
        for light_obj in light_objects:
            light += (max(np.dot(-np.array(light_obj.get_dir(intersection_pos)), normal_dir), 0)
                      * (not self.shadow(intersection_pos, light_obj))
                      * light_obj.power)
        light = minmax(light, 0, 1)  # уровень освещённости не может быть больше 1 и меньше 0
        return light
    
    def shadow(self, position: Sequence[Union[int, float]], light: BaseLight):
        """
        Определяет, падает ли на объект тень от других объектов. Тень определяется только от одного источника света.
        :param position: точка, на которой надо проводить проверку на наличие тени.
        :param light: объект источника света
        :return: True, если тень падает на объект, иначе False
        """
        shadow_ray = -np.array(light.get_dir(position))
        light_dist = light.get_distance(position)
        for obj in figures_objects:
            if obj == self:
                continue
            is_intersect, intersection_dist, normal = obj.intersect(position, shadow_ray)
            if is_intersect and intersection_dist < light_dist:  # если есть объект, стоящий между исходным объектом и источником света
                return True                                      # вернуть True, тень есть
        return False

