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
    {"type": "sphere", "position": [0, 0, 0], "radius": 0.3, "color": {"reflects": False}},
    {"type": "sphere", "position": [0.4, -0.07, 0], "radius": 0.075, "color": {"reflects": False}},
    {"type": "box", "position": [0, 1, 0], "size": [0.3, 0.3, 0.3], "color": {"reflects": False}},
    {"type": "plane", "direction": [0, 0, -1], "z_position": 0.3, "color": {"reflects": False}},
    {"type": "sun", "direction": [-0.7, 0.2, 0.5], "power": 1},  # направленное освещение
    {"type": "ambient_light", "power": 0.05},  # рассеянное освещение
    {"type": "point_light", "position": [1, 0.8, -0.05], "power": 0.45}
]

def minmax(value, min_, max_):
    """Ограничение числа value сверху и снизу числами min_ и max_"""
    return max(min(value, max_), min_)

def vector_length(vector: list):
    """Определяет длину вектора по теореме Пифагора"""
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def normalize(vector: list|np.ndarray):
    """Нормализация вектора"""
    length = vector_length(vector)
    return [vector[0]/length, vector[1]/length, vector[2]/length]

def sign(value):
    """Определяет знак числа или всех чисел в списке
    :return 0 если 0, -1 если отрицательное, 1 если положительное"""
    if type(value) == list or type(value) == np.ndarray:
        a = []
        for i in list(value):
            # print(i, value)
            a.append((0 < float(i)) - (float(i) < 0))
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
                m.append(50)  # небольшой костыль, который убирает чёрную полоску с куба
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

def plane_intersect(ro: list, rd: list, pd: list, z_position):
    """
    Функция пересечения луча с плоскостью
    :param ro: координаты начала луча
    :param rd: вектор направления луча
    :param pd: вектор направления плоскости
    :param z_position: позиция плоскости по оси z
    :return: False если пересечения нет, расстояние от точки пересечения до начала луча если нет
    """
    a = -(np.dot(ro, normalize(pd)) + z_position) / np.dot(rd, pd)
    if a >= 0:
        return a
    return False


def lighting(nd: list, ip: list, oi: int):
    """
    Определяет освещённость определённой точки
    :param nd: вектор направления нормали
    :param ip: координаты точки пересечения луча с объектом
    :param oi: номер объекта
    :return: число, характеризующее освещённость
    """
    light = 0
    for light_obj in objects:  # цикл для разных источников света
        if light_obj["type"] == "sun":  # освещения "солнца"
            light += (max(np.dot(-np.array(normalize(light_obj["direction"])), nd), 0)
                      * 0.65
                      * (not shadow(ip, light_obj["direction"], oi))
                      * light_obj["power"])
        elif light_obj["type"] == "ambient_light":  # освещение окружения
            light += light_obj["power"]  # тупо прибавляем силу освещения
            # по-хорошему вместо освещения окружения нужно делать диффузное отражения для матовых объектов, но это
            # будет слишком долго просчитываться, а ещё мне лень над этим париться
        elif light_obj["type"] == "point_light":
            light_dir = normalize(ip - np.array(light_obj["position"]))  # направление до источника света
            light += (max(np.dot(-np.array(light_dir), nd), 0)
                      * 0.65
                      * (not shadow(ip, light_dir, oi, "point_light", light_obj["position"]))
                      * light_obj["power"])
    return light

def reflects(ro: list|np.ndarray, rd: list|np.ndarray, nd: list, oi: int = -1, ri: int = 0):
    """Отражает луч для рисования отражений
    :param ro: координаты начало луча
    :param rd: вектор направления оригинального луча
    :param nd: вектор направления нормали объекта
    :param oi: номер объекта, от которого отразился луч
    :param ri: номер переотражения
    :return: уровень освещённости места отражения
    """
    reflected_dir = np.array(rd) - 2 * np.dot(nd, rd) * np.array(nd)
    reflected_light = lighting(-reflected_dir, ro, oi)**16
    min_distance = 9999
    for reflected_obj_id in range(len(objects)):
        if reflected_obj_id == oi:
            continue
        reflected_obj = objects[reflected_obj_id]
        reflected_obj_distance = False
        if reflected_obj["type"] == "sphere":
            reflected_obj_distance = sphere_intersect(reflected_obj["position"], reflected_obj["radius"],
                                                      list(ro), reflected_dir)
            if reflected_obj_distance >= min_distance or not reflected_obj_distance:
                continue
            reflected_intersection_pos = np.array(np.array(ro) + np.array(reflected_dir) * reflected_obj_distance)
            reflected_normal_dir = normalize(reflected_intersection_pos - np.array(reflected_obj["position"]))
            if reflected_obj["color"]["reflects"] and ri < 2:  # отражения
                reflected_light_2 = reflects(reflected_intersection_pos, reflected_dir, reflected_normal_dir, reflected_obj_id, ri+1)
            else:
                reflected_light_2 = 0
        elif reflected_obj["type"] == "box":
            reflected_obj_distance, reflected_normal_dir = box_intersect(list(ro), reflected_dir,
                                                                         reflected_obj["size"],
                                                                         reflected_obj["position"])
            if reflected_obj_distance >= min_distance or not reflected_obj_distance:
                continue
            reflected_intersection_pos = np.array(np.array(ro) + np.array(reflected_dir) * reflected_obj_distance)
            if reflected_obj["color"]["reflects"] and ri < 2:  # отражения
                reflected_light_2 = reflects(reflected_intersection_pos, reflected_dir, reflected_normal_dir, reflected_obj_id, ri+1)
            else:
                reflected_light_2 = 0
        elif reflected_obj["type"] == "plane":
            reflected_obj_distance = plane_intersect(ro, reflected_dir, reflected_obj["direction"],
                                                     reflected_obj["z_position"])
            if reflected_obj_distance >= min_distance or not reflected_obj_distance:
                continue
            reflected_normal_dir = reflected_obj["direction"]
            reflected_intersection_pos = np.array(np.array(ro) + np.array(reflected_dir) * reflected_obj_distance)
            if reflected_obj["color"]["reflects"] and ri < 2:  # отражения
                reflected_light_2 = reflects(reflected_intersection_pos, reflected_dir, reflected_normal_dir, reflected_obj_id, ri+1)
            else:
                reflected_light_2 = 0
        if reflected_obj_distance and reflected_obj_distance < min_distance:
            min_distance = reflected_obj_distance
            reflected_light += lighting(reflected_normal_dir, reflected_intersection_pos, reflected_obj_id)*0.75
            reflected_light += reflected_light_2
    return reflected_light

def shadow(ip: list|np.ndarray, ld: list, oi: int, lt: str = "sun", lp: list = []):
    """
    Определяет, отбрасывается ли на объект тень
    :param ip: позиция точки пересечения объекта с лучом света
    :param ld: вектор направления света
    :param oi: номер объекта, на который должна падать или не падать тень
    :param lt: тип источника света, если не указан, то sun
    :param lp: координаты источника света
    :return: True если тень падает, False если нет
    """
    shadow_ray_dir = -np.array(ld)
    nearest_dist = 9999
    if lt != "sun":
        light_distance = vector_length(np.array(ip) - lp)
    for obj_id in range(len(objects)):
        obj = objects[obj_id]
        if obj_id == oi:
            continue
        if obj["type"] == "sphere":
            if distance := (sphere_intersect(obj["position"], obj["radius"], ip, shadow_ray_dir)):
                if lt == "sun":
                    return True
                if distance < nearest_dist and distance < light_distance:
                    nearest_dist = distance
        elif obj["type"] == "box":
            if distance := (box_intersect(ip, shadow_ray_dir, obj["size"], obj["position"])[0]):
                if lt == "sun":
                    return True
                if distance < nearest_dist and distance < light_distance:
                    nearest_dist = distance
        elif obj["type"] == "plane":
            if distance := (plane_intersect(ip, shadow_ray_dir, obj["direction"], obj["z_position"])):
                if lt == "sun":
                    return True
                if distance < nearest_dist and distance < light_distance:
                    nearest_dist = distance
    if nearest_dist != 9999 and lt != "sun":
        return True
    return False

def frame(time_, camera_pos, camera_dir):
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
            for obj_id in range(len(objects)):
                obj = objects[obj_id]
                light = 0
                if obj["type"] == "sphere":  # пересечения со сферой
                    sphere_distance = sphere_intersect(obj["position"], obj["radius"], camera_pos, ray_dir)
                    if sphere_distance:
                        intersection_pos = np.array(np.array(camera_pos) + np.array(ray_dir) * sphere_distance)
                        normal_dir = normalize(intersection_pos - np.array(obj["position"]))
                        light += lighting(normal_dir, list(intersection_pos), obj_id)
                        if obj["color"]["reflects"] and sphere_distance < min_distance:  # отражения
                            light *= 0.5
                            reflected_light = reflects(intersection_pos, ray_dir, normal_dir, obj_id, 0)
                        else:
                            reflected_light = 0
                        if sphere_distance < min_distance:
                            min_distance = sphere_distance
                            draw_light = light + reflected_light
                elif obj["type"] == "box":  # пересечения с параллелепипедом
                    box_distance, normal_dir = box_intersect(camera_pos, ray_dir, obj["size"], obj["position"])
                    if box_distance:
                        intersection_pos = np.array(np.array(camera_pos) + np.array(ray_dir) * box_distance)
                        light += lighting(normal_dir, list(intersection_pos), obj_id)
                        if obj["color"]["reflects"] and box_distance < min_distance:  # отражения
                            light *= 0.5
                            reflected_light = reflects(intersection_pos, ray_dir, normal_dir, obj_id, 0)
                        else:
                            reflected_light = 0
                        if box_distance < min_distance:
                            min_distance = box_distance
                            draw_light = light + reflected_light
                elif obj["type"] == "plane":  # пересечения с плоскостью
                    normal_dir = obj["direction"]
                    plane_distance = plane_intersect(camera_pos, ray_dir, obj["direction"], obj["z_position"])
                    if plane_distance:
                        intersection_pos = np.array(np.array(camera_pos) + np.array(ray_dir) * plane_distance)
                        light += lighting(normal_dir, list(intersection_pos), obj_id)
                        if obj["color"]["reflects"] and plane_distance < min_distance:  # отражения
                            light *= 0.5
                            reflected_light = reflects(intersection_pos, ray_dir, normal_dir, obj_id, 0)
                        else:
                            reflected_light = 0
                        if plane_distance < min_distance:
                            min_distance = plane_distance
                            draw_light = light + reflected_light
            screen += gradient_symbols[minmax(round(draw_light * 15), 0, 10)]  # рисование пикселя
    sys.stdout.write(screen)  # рисование кадра
    sys.stdout.flush()


timer = 0
camera_direction = normalize([-1, 0, 0])
camera_position = [1, 0, 0]
mode = False

def update(a: bool = False):  # псевдоним для функции frame с параметрами для простого использования
    if (not a and mode) or (a and not mode):
        frame(timer, camera_position, camera_direction)  # [-math.sin(timer*0.1), -math.cos(timer*0.1), 1]

os.system('cls' if os.name == 'nt' else 'clear')  # очистка терминала
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
            camera_position = np.array(camera_position) + np.array(camera_direction) * 0.1
            update()
        if keyboard.is_pressed("down"):
            mov_dir = [-camera_direction[0], -camera_direction[1], camera_direction[2]]
            camera_position = np.array(camera_position) + np.array(mov_dir) * 0.1
            update()
        if keyboard.is_pressed("a"):
            mov_dir = [camera_direction[0] * math.cos(math.radians(90)) - camera_direction[1] * math.sin(math.radians(90)),
                       camera_direction[0] * math.sin(math.radians(90)) + camera_direction[1] * math.cos(math.radians(90)),
                       0]
            camera_position = np.array(camera_position) + np.array(mov_dir) * 0.1
            update()
        if keyboard.is_pressed("d"):
            mov_dir = [camera_direction[0] * math.cos(math.radians(-90)) - camera_direction[1] * math.sin(math.radians(-90)),
                       camera_direction[0] * math.sin(math.radians(-90)) + camera_direction[1] * math.cos(math.radians(-90)),
                       0]
            camera_position = np.array(camera_position) + np.array(mov_dir) * 0.1
            update()
    except:
        break
    timer += 1
    update(True)
