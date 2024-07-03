from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Capsule(BaseFigure):
    """The capsule is a cylinder, but with caps in the form of hemispheres"""
    def __init__(self,
                 radius: Union[int, float],
                 cap0: Sequence[float],
                 cap1: Sequence[float],
                 reflects: Union[float, int] = 0,
                 visible: bool = True
                 ) -> NoReturn:
        """
        Creating a capsule object based on the coordinates of its caps
        :param radius: the radius of the capsule
        :param cap0: coordinates of the first cap
        :param cap1: coordinates of the second cap
        :param reflects: the ability of an object to reflect other objects (work as a mirror)
        :param visible: will this figure be rendered
        """
        super().__init__([], [0.0, 0.0, -1.0], radius, reflects, visible)
        self.radius = radius
        self.a = np.array(cap0)
        self.b = np.array(cap1)

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

        oa = ro - self.a
        bard = np.dot(self.ba, rd)
        baoa = np.dot(self.ba, oa)
        rdoa = np.dot(rd, oa)
        oaoa = np.dot(oa, oa)
        a = self.baba - bard * bard
        b = self.baba * rdoa - baoa * bard
        c = self.baba * oaoa - baoa * baoa - self.rarababa
        h = b * b - a * c
        if h >= 0:
            t = (-b - math.sqrt(h)) / a
            y = baoa + t * bard
            if 0.0 < y < self.baba:
                return True, t, self.normal_dir(ro + np.array(rd) * t)
            if y<= 0:
                oc = oa
            else:
                oc = ro - self.b
            b = np.dot(rd, oc);
            c = np.dot(oc, oc) - self.radius * self.radius
            h = b * b - c
            if h > 0.0:
                di = -b - math.sqrt(h)
                return True, di, self.normal_dir(ro + np.array(rd) * di)
        return False, -1.0, [0.0, 0.0, -1.0]

    def normal_dir(self, intersection_pos: Sequence[float]) -> Sequence[float]:
        pa = intersection_pos - self.ba
        h = minmax(np.dot(pa, self.ba) / self.baba, 0.0, 1.0)
        return (pa - h * self.ba) / self.radius
