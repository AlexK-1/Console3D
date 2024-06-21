from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence
import numpy as np
import math

from ..base import BaseObject3D
from ..objs_list import light_objects, figures_objects
from ..lighting.base import BaseLight
from ...utils import *
from .shadows_cache import shadows_cache
from ...config import debug


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
        try:
            len(size)
            self.size = np.array(size)
        except TypeError:
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
        return [0.0, 0.0, 0.0]
    
    def lightning(self, normal_dir: Sequence[float], intersection_pos: Sequence[Union[int, float]], pixel_x: int = -1) -> float:
        """
        Определяет освещённость точки на объекте. Подразумевается, что пересечение объекта с лучом есть.
        :param normal_dir: вектор направления нормали
        :param intersection_pos: координаты точки пересечения луча с объектом
        :param pixel_x: номер пикселя по оси x, нужно для кэширования теней
        :return: освещённость точки от 0 до 1
        """
        if len(light_objects) == 0:
            return 0
        
        light = 0
        for light_obj in light_objects:
            light += (max(np.dot(-(light_obj.get_dir(intersection_pos)), normal_dir), 0)
                      * (not self.shadow(intersection_pos, light_obj, pixel_x=pixel_x))
                      * light_obj.power)
        light = minmax(light, 0, 1)  # уровень освещённости не может быть больше 1 и меньше 0
        return light
    
    def shadow(self, position: Sequence[Union[int, float]], light: BaseLight, pixel_x: int = -1):
        """
        Определяет, падает ли на объект тень от других объектов. Тень определяется только от одного источника света.
        :param position: точка, на которой надо проводить проверку на наличие тени.
        :param light: объект источника света
        :param pixel_x: номер пикселя по оси x, нужно для кэширования теней
        :return: True, если тень падает на объект, иначе False
        """

        shadow_ray_ = -(light.get_dir(position))
        light_dist = light.get_distance(position)

        if pixel_x >= 0:
            left_shadow = shadows_cache[pixel_x - 1] if (pixel_x > 0 and len(shadows_cache) > 0) else None
            if left_shadow:
                is_intersect, intersection_dist, normal = left_shadow.intersect(position, shadow_ray_)
                if is_intersect and intersection_dist < light_dist:
                    shadows_cache[pixel_x] = left_shadow
                    return True
            right_shadow = shadows_cache[pixel_x + 1] if len(shadows_cache) > (pixel_x+1) else None
            if right_shadow and right_shadow != left_shadow:
                is_intersect, intersection_dist, normal = right_shadow.intersect(position, shadow_ray_)
                if is_intersect and intersection_dist < light_dist:
                    shadows_cache[pixel_x] = right_shadow
                    return True
            up_shadow = shadows_cache[pixel_x] if len(shadows_cache) > pixel_x else None
            if up_shadow and up_shadow not in (left_shadow, right_shadow):
                is_intersect, intersection_dist, normal = up_shadow.intersect(position, shadow_ray_)
                if is_intersect and intersection_dist < light_dist:
                    shadows_cache[pixel_x] = up_shadow
                    return True
        else:
            left_shadow = None
            up_shadow = None
            right_shadow = None
            # print("Тени от объектов на пиксели соседи в кэше:", left_shadow, up_shadow, right_shadow)

        for obj in figures_objects:
            if obj == self or obj in (left_shadow, up_shadow, right_shadow):
                continue
            is_intersect, intersection_dist, normal = obj.intersect(position, shadow_ray_)
            if is_intersect and intersection_dist < light_dist:  # если есть объект, стоящий между исходным объектом и источником света
                shadows_cache[pixel_x] = obj
                return True                                      # вернуть True, тень есть
        shadows_cache[pixel_x] = None
        return False

    # def shadow(self, position: Sequence[Union[int, float]], light: BaseLight, pixel_x: int = -1):
    #     """
    #     Определяет, падает ли на объект тень от других объектов. Тень определяется только от одного источника света.
    #     :param position: точка, на которой надо проводить проверку на наличие тени.
    #     :param light: объект источника света
    #     :param pixel_x: номер пикселя по оси x, нужно для кэширования теней
    #     :return: True, если тень падает на объект, иначе False
    #     """
    #     global shadows_cache
    #
    #     shadow_ray_ = -(light.get_dir(position))
    #     light_dist = light.get_distance(position)
    #
    #     if shadows_cache and self != shadows_cache:
    #         try:
    #             is_intersect, intersection_dist, _ = shadows_cache.intersect(position, shadow_ray_)
    #         except AttributeError:
    #             is_intersect = False
    #         if is_intersect and intersection_dist < light_dist:  # если есть объект, стоящий между исходным объектом и источником света
    #             return True
    #
    #     for obj in figures_objects:
    #         if obj == self or obj == shadows_cache:
    #             continue
    #         is_intersect, intersection_dist, _ = obj.intersect(position, shadow_ray_)
    #         if is_intersect and intersection_dist < light_dist:  # если есть объект, стоящий между исходным объектом и источником света
    #             shadows_cache = obj
    #             return True                                      # вернуть True, тень есть
    #     shadows_cache = None
    #     return False
