# Console3D

This project is capable of drawing simple **3D graphics** into a terminal/console **using symbols**.
The rendering is carried out according to the [raytracing](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)) algorithm.

![3D graphics in the terminal](https://github.com/AlexK-1/AlexK-1/assets/154962283/3f9969c9-a648-4a59-b32f-5f1d47ada991)

# Getting started

Enter these commands in terminal\shell to clone this repository and install the necessary libraries:
```shell
git clone https://github.com/AlexK-1/Console3D.git
pip install -r requirements.txt
```
In the newly created folder, create a file (for example, `main.py `)
and write the code for creating and rendering a 3D scene in it,
to get started, you can take the code from
the *Example usage* section.

In the file `Console3D/config.py` you can specify the height
and width (in characters) of the terminal/console
(`width` and `height`), as well as the width and height of one
character (in pixels) of the terminal/console `font_width`
and `font_height`. You can get these settings in the terminal
and font settings.
You can also specify the maximum number of re-reflections
(`max_re_reflections`).

```python
from Console3D import config

config.width = 120  # Terminal/console width
config.height = 500  # Terminal/console height
config.font_width = 8  # Font width
config.font_height = 16  # Font height
```

# Example usage

```py
from Console3D import objects3D, draw_frame  # importing an internal library
from Console3D.objects3D import figures, lighting


camera = objects3D.Camera([1, 0.2, 0], [-1, 0.2, 0.0])  # creating a camera object

# creating visible figures
sphere = figures.Sphere([0, 0, 0], 0.3)
sphere2 = figures.Sphere([0.4, -0.07, 0], 0.075)
box = figures.Box([0, 1, 0], [1, 0, 0], [0.3, 0.3, 0.3])
plane = figures.Plane([0, 0, -0.3], [0.0, 0.0, 1.0])

light = lighting.PointLight([0.7, 0.2, 1], 1)  # creating lighting

draw_frame()  # drawing a single frame to the terminal/console
```

# 3D objects

All 3D objects are inherited from the class
`Console3D.objects3D.base.BaseObject3D`. Any 3D object has a position and
direction (the direction can be expressed as a vector or as a list of degrees along three axes) parameter, but not all objects use them.

The `pos` method contains the coordinates of the object,
and the `dir` method contains the direction.

You can use the `rotate_x`, `rotate_y` and `rotate_z` methods to rotate
an object around a certain axis, but only if the direction of the object is a vector.

```python
from Console3D.objects3D.base import BaseObject3D


some_object = BaseObject3D([0, 0, 0], [1.0, 0.0, 0.0])  # creating an object

some_object.pos  # position
some_object.dir  # direction

some_object.rotate_x(90)  # rotate an object around the X axis
some_object.rotate_y(-90)  # rotate an object around the Y axis
some_object.rotate_z(180)  # rotate an object around the Z axis
```

## Figures

Figures are 3D objects that you can see.
There are 6 figures in the `Console3D` library as standard: sphere,
box, plane, polygone, cylinder, capsule, but you can add your own figures classes as well.
The ready-made figures classes and the base figure class are located
in the `Console3D.objects3D.figures`.

To add a figure to the scene, you must call the constructor
of the class of this figure, for example, you can create a variable
with an instance of the shape class for convenient interaction with it.

```python
from Console3D.objects3D import figures

sphere = figures.Sphere([0, 0, 0], 0.3)
box = figures.Box([0, 1, 0], [1, 0, 0], [0.3, 0.3, 0.3])
plane = figures.Plane([0, 0, -0.3], [0.0, 0.0, 1.0])
polygon = figures.Polygon([0, 0, 0], [0, 0.3, 0], [0, 0, 0.4])
cylinder = figures.Cylinder(0.2, [0, -0.4, 0.2], [0, 0.2, 0])
capsule = figures.Capsule(0.2, [0, -0.4, 0.2], [0, 0.2, 0])
```

All figures have parameters `visibility` and the ability to reflect
light (`reflections`). The figures have a position, some
direction (in the form of a vector) and a size.

### Sphere

The class `Console3D.objects3D.figures.Sphere` is drawn as
a perfectly flat sphere and has 4 parameters: `position`
coordinates of the center of the sphere in three-dimensional space,
`diameter`, `reflects` from 0 to 1 denotes the degree of specularity,
`visible` if `false`, then the sphere will be invisible.

```python
from Console3D.objects3D import figures

sphere = figures.Sphere([x_position, y_position, z_position],
                        reflections, visible)
```

### Box
The class `Console3D.objects3D.figures.Box` looks like a
rectangular parallelepiped, it accepts the parameters `position`,
`direction` as a vector of the direction of one of its faces
*(does not work)*, `size` as a list of box sizes along
the X, Y and Z axes, `reflects`, `visible`.

```python
from Console3D.objects3D import figures

box = figures.Box([x_position, y_position, z_position],
                  direction, [x_size, y_size, z_size],
                  reflections, visible)
```

### Plane
The class `Console3D.objects3D.figures.Plane` looks like an
infinite plane, it accepts the parameters: `position` as
coordinates of any point of the plane, `direction` as the vector
direction of the plane, `reflects`, `visible`.

```python
from Console3D.objects3D import figures

plane = figures.Plane([x_position, y_position, z_position],
                      direction, reflections, visible)
```

### Polygone
The class `Console3D.objects3D.figures.Polygon` is a triangular
polygon defined by the coordinates of the three vertices
`vertex0`, `vertex1` and `vertex2`, and the class also accepts
the parameters `reflects` and `visible`.

```python
from Console3D.objects3D import figures

polygon = figures.Polygon(first_vertex_pos, second_vertex_pos,
                          third_vertex_pos, reflections, visible)
```

### Cylinder
The class `Console3D.objects3D.figures.Cylinder` is a cylinder bounded
with two circular planes. It accepts the parameters `radius`,
`face0` coordinates of the first face, `face1` coordinates
of the second face, `reflects`, `visible`.

```python
from Console3D.objects3D import figures

cylinder = figures.Cylinder(radius, first_face_pos, second_face_pos,
                         reflections, visible)
```

### Capsule
The `Console3D.objects3D.figures' class.Capsule` looks like
a cylinder with hemispheres instead of flat caps. Accepts
the parameters `radius`, `cap0` and `cap1` coordinates of the
covers, `reflections` and `visible`.

```python
from Console3D.objects3D import figures

cylinder = figures.Cylinder(radius, first_cap_pos, second_cap_pos, 
                            reflections, visible)
```

### Your figures
To create your own figure, you must create a class inherited
from the base figure class
`Console3D.objects3D.figures.base.BaseFigure`. Your class should
preferably have the `reflections` and `visible` parameters.
In the class constructor, you must call the `BaseFigure` constructor.
If your shape has a direction, and it is a vector, you should normalize it.

In order for your figure to be drawn, you need to create the
`ray_intersection_fn` method in your figure class, it determines
whether the ray intersects with your figure, it takes two
parameters: the coordinates of the beginning of the ray and
the vector of the direction of the ray, the method should return
three values: the boolean value of the intersection,
the distance from the beginning of the ray to the intersection
point and the direction of the normal figure at the
intersection point.

You can also add the `normal_dir` method to your class,
which determines the direction of the normal at a certain
point and use this method in the `ray_intersection_fn` method.

Example:
```python
from typing import Union, NoReturn, Tuple, Sequence
from Console3D.objects3D.figures.base import BaseFigure
from Console3D.vec_functions import normalize


class MyFigure(BaseFigure):
    def __init__(self,  # In this example, there is no `size` parameter specifically
                 position: Sequence[Union[int, float]],
                 direction: Sequence[float],
                 reflects: Union[float, int] = 0,
                 visible: bool = True) -> NoReturn:
        super().__init__(position, normalize(direction), 1, reflects, visible)  # the direction is normalized because it is a vector
    def ray_intersection_fn(self, ro: Sequence[Union[int, float]],
                            rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        """
        ro - coordinates of the origin of the ray
        rd - vector direction of the ray
        """
        ...  # The code for determining the intersection
        return presence_of_intersection, distance_to_intersection, normal_direction
```

## Lighting
Lighting objects cannot be seen, but they give light and allow
you to see other objects. Without lighting, the scene will look
completely black.

Creating lighting objects is similar to creating figures.
To create a light source, you need to call the constructor
of the class of this light source and preferably assign
it to a variable.

```python
from Console3D.objects3D import lighting


light = lighting.DirectionalLight([-0.7, 0.2, -0.5], 0.5)
light_2 = lighting.PointLight([0.7, 0.2, 1], 0.5)
```

All light sources have the `power` parameter,
which determines the light intensity from 0 to 1,
some light sources have a position and direction.

> [!TIP]
> To prevent the scene from being too bright or dark,
> it is better to adjust the light sources so that the sum
> of the total light power is equal to 1.

### Directional light
Class `Console3D.objects3D.lightning.DirectionalLight`.
This light source has a direction, but no position.
It is an imitation of the sun.

Directional light has two parameters: `direction` and `power`.

```python
from Console3D.objects3D import lighting


light = lighting.DirectionalLight(direction, power)
```

### Point light
Class `Console3D.objects3D.lightning.PointLight`.
Point light, unlike directional light, has only position,
but does not have a direction. This means that it shines
in all directions. A point light can be compared to a glowing
light bulb.

It takes two parameters: `position` and `power`.

```python
from Console3D.objects3D import lighting


light = lighting.PointLight([x_position, y_position, z_position], power)
```

### Your light sources

To create your own light source object, you need to create
a class inherited from the base class of lighting sources
`Console3D.objects3D.lightning.base.BaseLight`. The required
parameter of your light source class is `power`, optional
parameters are `direction` (should be normalized if the vector is) and `position`.

In the constructor of your light source class, you must call
the constructor of the parent class, and in addition to the
constructor, your class must have 2 methods: `get_distance` to
determine the distance from the point to the light source and
`get_dir` to determine the direction vector of the light.
The `get_distance` method should return an integer or
fractional number, and `get_dir` should return the direction
as a vector by the `numpy.ndarray` class.

What should your class look like using the example of a point light:
```python
from typing import Union, Sequence, NoReturn
import numpy as np
from Console3D.objects3D.lighting.base import BaseLight
from Console3D.vec_functions import normalize, vector_length


class MyLight(BaseLight):  # It has no direction
    def __init__(self, position: Sequence[Union[float, int]], power: Union[int, float]) -> NoReturn:
        super().__init__(position, [0.0, 0.0, -1.0], power)
    
    def get_dir(self, position) -> np.ndarray:  #        # It shines in all directions, so the direction
        return normalize(position - np.array(self.pos))  # is calculated relative to the `position` coordinates
    
    def get_distance(self, position) -> float:
        return vector_length(np.array(position) - self.pos)
```

## Camera
The camera is where the image is rendered from, where you see your scene from. 
You can't see the camera. The camera must be on the stage, otherwise
rendering of the scene will be impossible. If you create multiple camera
objects, only the last one created will be used.

The camera has `position` and `direction` (vector) parameters.

```python
from Console3D import objects3D


camera = objects3D.Camera([x_position, y_position, z_position], direction)
```

# Rendering
The scene is rendered and displayed using the `draw_frame` function of
the `Console3D` library. The function does not accept arguments and
returns FPS, it prints a picture of characters to the console/terminal.
The rendering of the scene directly depends on the camera object.
If there is no camera, there will be no render.

```python

from Console3D import objects3D, draw_frame


camera = objects3D.Camera([x_position, y_position, z_position], direction)

# Creating figures and lighting sources

draw_frame()
```

# Credits
I decided to create this project by watching a video on @ArtemOnigiri
YouTube. He has his own [repository](https://github.com/ArtemOnigiri/Console3D) with 3D graphics in the console,
written in C and C++