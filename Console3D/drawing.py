from typing import NoReturn, Sequence, Union
import math
import numpy as np
import sys

from .config import *
from .utils import *
from .vec_functions import *
from .objects3D.objs_list import camera_object, figures_objects
from .objects3D.figures.base import BaseFigure


gradient_symbols = " .:!/(l1Z4H9W8$@"


def draw_frame() -> NoReturn:
    """Отрисовывает один кадр."""
    camera = camera_object[0]
    screen = ""
    for symbol_y in range(height):
        for symbol_x in range(width):
            x = (symbol_x / height) * (font_width / font_height) - ((width / height) * (font_width / font_height) / 2)
            y = symbol_y / height - 0.5  # приведение координат пикселя к значениям, близким к 1 0 -1

            ray_dir = rotate_vector_z(camera.dir, -55*x)  # определение направления луча
            ray_dir[2] = -y
            ray_dir = normalize(ray_dir)

            draw_light = ray(camera.pos, ray_dir)
            screen += gradient_symbols[round(draw_light*(len(gradient_symbols)-1))]
    sys.stdout.write(screen)  # рисование кадра
    sys.stdout.flush()

def ray(ro: Sequence[Union[float, int]], rd: Sequence[float], ray_id: int = 0, reflective_object: BaseFigure = None) -> float:
    """
    Определяет яркость определённой точки, "бросает" луч в определённом направлении.
    :param ro: точки, из которой идёт луч
    :param rd: направление луча
    :param ray_id: номер луча, нужно, чтобы луч не мог отражаться бесконечное кол-во раз
    :return: яркость от 0 до 1
    """
    min_distance = math.inf
    draw_light = 0
    for object in figures_objects:
        if reflective_object and object == reflective_object:
            continue
        is_intersect, intersection_dist, normal = object.intersect(ro, rd)
        if is_intersect and intersection_dist < min_distance:
            min_distance = intersection_dist
            intersection_pos = np.array(np.array(ro) + np.array(rd) * intersection_dist)
            draw_light = object.lightning(normal, intersection_pos)
            if object.reflects > 0 and ray_id < max_re_reflections:
                draw_light *= (1 - object.reflects)
                reflected_dir = reflect(rd, normal)
                draw_light += (ray(intersection_pos, reflected_dir, ray_id+1, object) + object.lightning(reflected_dir, intersection_pos) ** 16) * object.reflects * 0.9
    return minmax(draw_light, 0, 1)
