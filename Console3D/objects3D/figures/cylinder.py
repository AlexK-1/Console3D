from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Cylinder(BaseFigure):
    """Straight cylinder"""
    def __init__(self,
                 radius: Union[int, float],
                 face0: Sequence[float],
                 face1: Sequence[float],
                 reflects: Union[float, int] = 0,
                 visible: bool = True
                 ) -> NoReturn:
        """
        Creating a cylinder based on the radius of its faces and their coordinates
        :param radius: the radius of the face
        :param face0: coordinates of the first face
        :param face1: coordinates of the second face
        :param reflects: the ability of an object to reflect other objects (work as a mirror)
        :param visible: will this figure be rendered
        """
        super().__init__([], [0.0, 0.0, -1.0], radius, reflects, visible)
        self.radius = radius
        self.a = np.array(face0)
        self.b = np.array(face1)

        self.ba = self.b - self.a
        self.baba = np.dot(self.ba, self.ba)
        self.rarababa = self.radius * self.radius * self.baba
        self.bara_pr = [self.b, self.a, self.radius]

    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        if not np.array_equal(self.bara_pr[0], self.b) or not np.array_equal(self.bara_pr[1], self.a) or self.bara_pr[2] != self.radius:
            self.ba = self.b - self.a
            self.baba = np.dot(self.ba, self.ba)
            self.rarababa = self.radius * self.radius * self.baba
            self.bara_pr = [self.b, self.a, self.radius]

        oc = ro - self.a
        bard = np.dot(self.ba, rd)
        baoc = np.dot(self.ba, oc)
        k2 = self.baba - bard * bard
        k1 = self.baba * np.dot(oc, rd) - baoc * bard
        k0 = self.baba * np.dot(oc, oc) - baoc * baoc - self.rarababa
        h = k1 * k1 - k2 * k0
        if h < 0.0:  #
            return False, -1, [0.0, 0.0, 0.0]
        h = math.sqrt(h)
        t = (-k1 - h) / k2
        y = baoc + t * bard
        if 0.0 < y < self.baba:
            return True, t, (oc+t * np.array(rd) - self.ba * y / self.baba) / self.radius
        if y < 0:
            l = 0
        else:
            l = self.baba
        t = (l - baoc) / bard
        if abs(k1 + k2 * t) < h:
            return True, t, self.ba * sign(float(y)) / math.sqrt(self.baba)
        return False, -1, [0.0, 0.0, 0.0]
