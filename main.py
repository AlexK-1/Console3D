import math
import keyboard
import numpy as np
import os
import sys
import time

width = os.get_terminal_size().columns  # автоматическое определение ширины и высоты терминала
height = os.get_terminal_size().lines
font_width = 8  # ширина и высота одного символа терминала (можно найти в свойствах терминала, раздел шрифт)
font_height = 16

gradient_symbols = " .:!/(l1Z4H9W8$@"

objects = [  # список объектов на сцене
    {"type": "sphere", "position": [0, 0, 0], "radius": 0.3},
    {"type": "sphere", "position": [0.4, -0.07, 0.1], "radius": 0.075},
    {"type": "box", "position": [0, 0.6, 0], "size": [0.2, 0.2, 0.2]},
]

def minmax(value, min_, max_):
    """Ограничение числа value сверху и снизу числами min_ и max_"""
    return max(min(value, max_), min_)

def vector_length(vector: list):
    """Определяет длину вектора по теореме Пифагора"""
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def normalize(vector: list):
    """Нормализация вектора"""
    length = vector_length(vector)
    return [vector[0]/length, vector[1]/length, vector[2]/length]

def sign(value):
    """Определяет знак числа или всех чисел в списке
    :return 0 если 0, -1 если отрицательное, 1 если положительное"""
    if type(value) == list:
        a = []
        for i in value:
            a.append((0 < i) - (i < 0))
        return a
    return (0 < value) - (value < 0)

def step(edge: list, x: list):
    """Определяет, больше значения списка x соответствующих значений списка edge
    :return Список чисел (0 если меньше или равно, 1 если больше)"""
    a = []
    for i in range(len(edge)):
        a.append(int(x[i] > edge[i]))
    return a


def sphere_intersect(center: list, radius: float, ray_origin: list, ray_direction: list):
    """Определяет наличие пересечения луча со сферой
    :param center координаты сферы
    :param radius радиус сферы
    :param ray_origin координаты начала луча (координаты камеры)
    :param ray_direction вектор направления луча
    :return False, если пересечений нет, расстояние до точки пересечения, если пересечение есть"""
    b = 2 * np.dot(ray_direction, np.array(ray_origin) - np.array(center))
    c = np.linalg.norm(np.array(ray_origin) - np.array(center)) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return False

def box_intersect(cp: list, rd: list, box_size: list, box_position: list):
    """
    Определяет наличие пересечения луча с параллелепипедом
    :param cp: координаты начала луча (позиция камеры)
    :param rd: вектор направления луча
    :param box_size: список размера параллелепипеда в трёх осях [x, y, z]
    :param box_position: координаты центра параллелепипеда
    :return: (False, False) если нет пересечения, расстояние до точки пересечения и вектор направления нормали, если есть
    """
    if 0 in rd:
        m = []
        for d in rd:
            if d != 0:
                m.append(1/d)
            else:
                m.append(50)
        m = np.array(m)
    else:
        m = np.ones(3) / np.array(rd)
    # print(m)
    n = m * (np.array(cp) - np.array(box_position))
    k = abs(m) * np.array(box_size)
    t1 = -n - k
    t2 = -n + k
    tn = max(max(t1[0], t1[1]), t1[2])
    tf = min(min(t2[0], t2[1]), t2[2])
    if tn > tf or tf < 0:
        return False, False
    yzx = [t1[1], t1[2], t1[0]]
    zxy = [t1[2], t1[0], t1[1]]
    out_normal = -np.array(sign(rd)) * np.array(step(yzx, t1)) * np.array(step(zxy, t1))
    return min(tn, tf), out_normal


def frame(time_, camera_pos, camera_dir, light_dir):
    screen = ""
    for symbol_y in range(height):
        for symbol_x in range(width):
            x = (symbol_x / height) * (font_width / font_height) - ((width / height) * (font_width / font_height) / 2)
            y = symbol_y / height - 0.5  # приведение координат пикселя к значениям, близким к 1 0 -1

            ray_dir = normalize([camera_dir[0]*math.cos(math.radians(x*-55)) - camera_dir[1]*math.sin(math.radians(x*-55)),
                                 camera_dir[0]*math.sin(math.radians(x*-55)) + camera_dir[1]*math.cos(math.radians(x*-55)),
                                 y])  # определение направления луча
            min_distance = 9999
            draw_light = 0
            for obj in objects:
                if obj["type"] == "sphere":  # пересечения со сферой
                    sphere_distance = sphere_intersect(obj["position"], obj["radius"], camera_pos, ray_dir)
                    if sphere_distance:
                        intersection_pos = np.array(np.array(camera_pos) + np.array(ray_dir) * sphere_distance)
                        normal_dir = normalize(intersection_pos - np.array(obj["position"]))
                        light = max(np.dot(-np.array(normalize(light_dir)), normal_dir), 0)
                        if sphere_distance < min_distance:
                            min_distance = sphere_distance
                            draw_light = light
                if obj["type"] == "box":  # пересечения с параллелепипедом
                    box_distance, normal_dir = box_intersect(camera_pos, ray_dir, obj["size"], obj["position"])
                    if box_distance:
                        light = max(np.dot(-np.array(normalize(light_dir)), normal_dir), 0)
                        if box_distance < min_distance:
                            min_distance = box_distance
                            draw_light = light
            screen += gradient_symbols[round(draw_light * 15)]  # рисование пикселя
    sys.stdout.write(screen)  # рисование кадра
    sys.stdout.flush()


timer = 0
camera_direction = [-1, 0, 0]
camera_position = [1, 0, 0]
# frame(timer, [1, 0, 0], camera_direction, [-0.75, -0.75, 1])

def update():  # псевдоним для функции frame с параметрами для простого использования
    frame(timer, camera_position, camera_direction,  [-0.5, 1, 1])  # [-math.sin(timer*0.1), -math.cos(timer*0.1), 1]

os.system('cls' if os.name == 'nt' else 'clear')
update()

while True:
    try:
        if keyboard.is_pressed("q"):  # управление с помощью клавиатуры
            print("Stop!")
            break
        if keyboard.is_pressed("right"):
            new_x = camera_direction[0] * math.cos(math.radians(-5)) - camera_direction[1] * math.sin(math.radians(-5))
            new_y = camera_direction[0] * math.sin(math.radians(-5)) + camera_direction[1] * math.cos(math.radians(-5))
            camera_direction = [new_x, new_y, camera_direction[2]]
            update()
        if keyboard.is_pressed("left"):
            new_x = camera_direction[0] * math.cos(math.radians(5)) - camera_direction[1] * math.sin(math.radians(5))
            new_y = camera_direction[0] * math.sin(math.radians(5)) + camera_direction[1] * math.cos(math.radians(5))
            camera_direction = [new_x, new_y, camera_direction[2]]
            update()
        if keyboard.is_pressed("up"):
            camera_position = np.array(camera_position) + np.array(camera_direction) * 0.05
            update()
        if keyboard.is_pressed("down"):
            mov_dir = [-camera_direction[0], -camera_direction[1], camera_direction[2]]
            camera_position = np.array(camera_position) + np.array(mov_dir) * 0.05
            update()
        if keyboard.is_pressed("a"):
            mov_dir = [camera_direction[0] * math.cos(math.radians(90)) - camera_direction[1] * math.sin(math.radians(90)),
                       camera_direction[0] * math.sin(math.radians(90)) + camera_direction[1] * math.cos(math.radians(90)),
                       0]
            camera_position = np.array(camera_position) + np.array(mov_dir) * 0.05
            update()
        if keyboard.is_pressed("d"):
            mov_dir = [camera_direction[0] * math.cos(math.radians(-90)) - camera_direction[1] * math.sin(math.radians(-90)),
                       camera_direction[0] * math.sin(math.radians(-90)) + camera_direction[1] * math.cos(math.radians(-90)),
                       0]
            camera_position = np.array(camera_position) + np.array(mov_dir) * 0.05
            update()
    except:
        break
    timer += 1
