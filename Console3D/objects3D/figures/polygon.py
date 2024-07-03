from abc import ABC
from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence, Optional
import math
import numpy as np

from .base import BaseFigure
from ...vec_functions import *
from ...utils import *


class Polygon(BaseFigure):
    """A triangular flat polygon. It is determined by the positions of its three vertices."""
    def __init__(self,
                 vertex0: Sequence[Union[int, float]],
                 vertex1: Sequence[Union[int, float]],
                 vertex2: Sequence[Union[int, float]],
                 reflects: Union[float, int] = 0,
                 visible: bool = True
                 ) -> NoReturn:
        """
        Creating a triangular polygon based on its three vertices.
        :param vertex0: coordinates of the first vertex
        :param vertex1: coordinates of the second vertex
        :param vertex2: coordinates of the third vertex
        :param reflects: the ability of an object to reflect other objects (work as a mirror)
        :param visible: will this figure be rendered
        """
        super().__init__([np.mean([vertex0[0], vertex1[0], vertex2[0]]), np.mean([vertex0[1], vertex1[1], vertex2[1]]), np.mean([vertex0[2], vertex1[2], vertex2[2]])],
                         [0.0, 0.0, -1.0],0.0, reflects, visible)
        self.vertex0 = np.array(vertex0)
        self.vertex1 = np.array(vertex1)
        self.vertex2 = np.array(vertex2)

        self.normal = self.normal_dir()
        self.v1v0 = self.vertex1 - self.vertex0
        self.v2v0 = self.vertex2 - self.vertex0
        self.n = np.cross(self.v1v0, self.v2v0)
        self.vertexes_pr = [self.vertex0, self.vertex1, self.vertex2]

    def ray_intersection_fn(self, ro: Sequence[Union[int, float]], rd: Sequence[float]) -> Tuple[bool, float, Sequence[float]]:
        if not np.array_equal(self.vertexes_pr[0], self.vertex0) or not np.array_equal(self.vertexes_pr[1], self.vertex1) or not np.array_equal(self.vertexes_pr[2], self.vertex2):
            self.normal = self.normal_dir()
            self.v1v0 = self.vertex1 - self.vertex0
            self.v2v0 = self.vertex2 - self.vertex0
            self.n = np.cross(self.v1v0, self.v2v0)
            self.vertexes_pr = [self.vertex0, self.vertex1, self.vertex2]

        rov0 = ro - self.vertex0
        q = np.cross(rov0, rd)
        d = 1.0 / np.dot(rd, self.n)
        u = d * np.dot(-q, self.v2v0)
        v = d * np.dot(q, self.v1v0)
        t = d * np.dot(-self.n, rov0)
        if u < 0.0 or v < 0.0 or (u + v) > 1.0:
            t = -1.0
        return (t > 0), t, self.normal

    def normal_dir(self) -> Sequence[float]:
        edge1 = np.array(self.vertex1) - np.array(self.vertex0)
        edge2 = np.array(self.vertex2) - np.array(self.vertex0)
        normal = np.cross(edge1, edge2)
        return normalize(normal)