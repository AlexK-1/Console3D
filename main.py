from Console3D import objects3D, draw_frame
from Console3D.objects3D import figures, lighting
from Console3D.vec_functions import normalize, rotate_vector_z

import numpy as np
import keyboard
import math
import os
import time


camera = objects3D.Camera([1, 0, 0], [-1, 0.0, 0.0])

sphere = figures.Sphere([0, 0, 0], 0.3)
sphere2 = figures.Sphere([0.4, -0.07, 0], 0.075)
box = figures.Box([0, 1, 0], [1, 0, 0], [0.3, 0.3, 0.3])
plane = figures.Plane([0, 0, -0.3], [0.0, 0.0, 1.0])

# light = lighting.DirectionalLight(normalize([-0.7, 0.2, -0.5]), 1)
light = lighting.PointLight([0.7, 0.2, 1], 1)

# all_fps = []
# for i in range(100):
#     all_fps.append(draw_frame())
# print("Mean FPS:", sum(all_fps)/len(all_fps))

draw_frame()

timer = 0
while True:
    try:
        if keyboard.is_pressed("q"):  # управление с помощью клавиатуры
            print("Stop!")
            break
        if keyboard.is_pressed("right"):
            camera.dir = rotate_vector_z(camera.dir, -5)
            # draw_frame()
        if keyboard.is_pressed("left"):
            camera.dir = rotate_vector_z(camera.dir, 5)
            # draw_frame()
        if keyboard.is_pressed("up"):
            camera.pos = np.array(camera.pos) + np.array(camera.dir) * 0.1
            # draw_frame()
        if keyboard.is_pressed("down"):
            mov_dir = [-camera.dir[0], -camera.dir[1], camera.dir[2]]
            camera.pos = np.array(camera.pos) + np.array(mov_dir) * 0.1
            # draw_frame()
        if keyboard.is_pressed("a"):
            mov_dir = rotate_vector_z(camera.dir, 90)
            camera.pos = np.array(camera.pos) + np.array(mov_dir) * 0.1
            # draw_frame()
        if keyboard.is_pressed("d"):
            mov_dir = rotate_vector_z(camera.dir, -90)
            camera.pos = np.array(camera.pos) + np.array(mov_dir) * 0.1
            # draw_frame()
    except:
        break
    timer += 1
    # box.pos[0] = math.sin(timer * 0.15)*1.5
    # box.pos[1] = math.cos(timer * 0.15)*1.5
    fps = draw_frame()
    time.sleep(max(1.0 / 60 - (1 / fps), 0))
