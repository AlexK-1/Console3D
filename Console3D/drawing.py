from typing import NoReturn, Sequence, Union
import math
import numpy as np
import sys
import time
import multiprocessing.dummy as mp
import os

from .config import *
from .utils import *
from .vec_functions import *
from .objects3D.objs_list import figures_objects
from .objects3D import objs_list
from .objects3D.figures.base import BaseFigure
from .objects3D.figures import cache


for i in range(width):
    cache.shadows_cache.append(None)

gradient_symbols = " .:!/(l1Z4H9W8$@"

font_proportion = (font_width / font_height)
screen_proportion = (width / height)
cache_width = (screen_proportion * font_proportion / 2)


# @log("Render frame")
# def draw_frame() -> NoReturn:
#     """Отрисовывает один кадр."""
#     camera = camera_object[0]
#     screen = []
#     start_time = time.time()
#     for symbol_y in range(height):
#         for symbol_x in range(width):
#             if symbol_y == 0:
#                 screen.append(" ")
#                 continue
#             x = (symbol_x / height) * (font_width / font_height) - ((width / height) * (font_width / font_height) / 2)
#             y = symbol_y / height - 0.5  # приведение координат пикселя к значениям, близким к 1 0 -1

#             ray_dir = rotate_vector_z(camera.dir, -55*x)  # определение направления луча
#             ray_dir[2] = -y
#             ray_dir = normalize(ray_dir)

#             if debug:
#                 print("_"*round(width*0.7))
#             draw_light = ray(camera.pos, ray_dir, pixel_x=symbol_x)
#             screen.append(gradient_symbols[round(draw_light*(len(gradient_symbols)-1))])  # добавление символа в кадр
#     end_time = time.time()
#     fps = 1/(end_time-start_time)
#     fps_string = f"FPS: {fps}"
#     screen[width:len(fps_string)+width] = fps_string

#     start_time = time.time()
#     screen = "".join(screen)
#     sys.stdout.write(screen)  # рисование кадра
#     sys.stdout.flush()
#     # os.write(screen)
#     print(f"Frame display: {time.time() - start_time}")
#     return fps

def draw_frame() -> NoReturn:
    """Отрисовывает один кадр."""
    screen = []
    start_time = time.time()
    
    # with mp.Pool() as p:
    screen = list(map(pixel, range(width * height)))

    end_time = time.time()
    try:
        fps = 1/(end_time-start_time)
    except ZeroDivisionError:
        fps = "Infinity"
    fps_string = f"FPS: {fps}"
    screen[width:len(fps_string)+width] = fps_string

    start_time = time.time()
    screen = "".join(screen)
    sys.stdout.write(screen)  # рисование кадра
    sys.stdout.flush()
    # os.write(screen)
    print(f"Frame display: {time.time() - start_time}")
    return fps

def pixel(pixel_id: int) -> str:
    """
    Вычисляет цвет одного пикселя и добавляет его на экран.
    :param pixel_id: id пикселя
    """
    global camera_object

    pixel_x = pixel_id % width
    pixel_y = pixel_id // width
    if pixel_y == 0:
        return " "
    x = (pixel_x / height) * font_proportion - cache_width
    y = (pixel_y / height) - 0.5  # приведение координат пикселя к значениям, близким к 1 0 -1

    ray_dir = rotate_vector_z(objs_list.camera_object.dir, -55*x)  # определение направления луча
    ray_dir[2] = -y
    ray_dir = normalize(ray_dir)

    draw_light = ray(objs_list.camera_object.pos, ray_dir)
    symbol = gradient_symbols[round(draw_light*(len(gradient_symbols)-1))]
    return symbol

def ray(
        ro: Sequence[Union[float, int]],
        rd: Sequence[float],
        ray_id: int = 0,
        reflective_object: BaseFigure = None,
        pixel_x: int = -1
       ) -> float:
    """
    Определяет яркость определённой точки, "бросает" луч в определённом направлении.
    :param ro: точки, из которой идёт луч
    :param rd: направление луча
    :param ray_id: номер луча, нужно, чтобы луч не мог отражаться бесконечное кол-во раз
    :param reflective_object: объект, от которого отражён луч
    :param pixel_x: номер пикселя по оси x, нужно для кэширования теней
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
            intersection_pos = ro + rd * intersection_dist
            draw_light = object.lightning(normal, intersection_pos, pixel_x=pixel_x)
            if object.reflects > 0 and ray_id < max_re_reflections:
                draw_light *= (1 - object.reflects)
                reflected_dir = reflect(rd, normal)
                draw_light += (ray(intersection_pos, reflected_dir, ray_id+1, object) + object.lightning(reflected_dir, intersection_pos, pixel_x=pixel_x) ** 16) * object.reflects * 0.9
    return minmax(draw_light, 0, 1)
