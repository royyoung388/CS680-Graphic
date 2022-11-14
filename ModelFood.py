"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

This class implements the bird model by
    - creating all components for the body
    - setting default rotation behavior for each component as well as rotation limits
    - linking components together in a hierarchy
Modified by Daniel Scrivener 07/2022
"""
import math

import ColorType as Ct
from EnvironmentObject import EnvironmentObject
from Point import Point
from Shapes import *

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class ModelFood(Component, EnvironmentObject):
    """
    Define our linkage model
    """

    components = None
    contextParent = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent
        self.components = []
        self.componentDict = {}
        self.rotation_speed = [-1, 1]
        self.translation_speed = 0.009

        # self.setDefaultScale([0.3, 0.3, 0.3])

        self.direction = Point((0, -1, 0)) * self.translation_speed
        # bounding
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.07
        self.species_id = 4

        food = Sphere(Point((0, 0, 0)), shaderProg, [0.07, 0.07, 0.07], Ct.RED)

        self.addChild(food)

        self.components.extend([food])
        self.componentDict.update({'food': food})

    def stepForward(self, components, tank_dimensions, vivarium):
        # move downward
        # drop to bottom
        if self.currentPos[1] + 2 <= self.bound_radius:
            self.direction = Point((0,0,0))
        self.setCurrentPosition(self.currentPos + self.direction)
