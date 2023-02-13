"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

import numpy as np

import ColorType
import GLUtility
from Component import Component
from DisplayableCube import DisplayableCube
from DisplayableCylinder import DisplayableCylinder
from DisplayableSphere import DisplayableSphere
from DisplayableTorus import DisplayableTorus
from Light import Light
from Material import Material
from Point import Point
from SceneBase import SceneBase


class SceneFour(Component, SceneBase):
    shaderProg = None
    glutility = None

    lights = None
    lightCubes = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        cube = Component(Point((0, -1, 1)), DisplayableCube(shaderProg, 0.5, color=ColorType.BLUE))
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.3, 0.3, 0.3, 0.3)), 64)
        cube.setMaterial(m1)
        cube.renderingRouting = "lighting"
        self.addChild(cube)

        cylinder = Component(Point((0, 1, 1)), DisplayableCylinder(shaderProg, 0.5, 0.2, color=ColorType.BLUE))
        m2 = Material(np.array((0.3, 0.3, 0.3, 0.3)), np.array((0.4, 0.4, 0.4, 1)),
                      np.array((0.5, 0.5, 0.5, 0.5)), 64)
        cylinder.setMaterial(m2)
        cylinder.renderingRouting = "lighting"
        self.addChild(cylinder)

        torus = Component(Point((0, 1, -1)), DisplayableTorus(shaderProg, 0.2, 0.5, color=ColorType.BLUE))
        m3 = Material(np.array((0.5, 0.5, 0.5, 0.5)), np.array((0.6, 0.6, 0.6, 1)),
                      np.array((0.7, 0.7, 0.7, 0.7)), 64)
        torus.setMaterial(m3)
        torus.renderingRouting = "lighting"
        self.addChild(torus)

        sphere = Component(Point((0, -1, -1)), DisplayableSphere(shaderProg, 0.2, color=ColorType.BLUE))
        m4 = Material(np.array((0.7, 0.7, 0.7, 0.7)), np.array((0.8, 0.8, 0.8, 1)),
                      np.array((0.9, 0.9, 0.9, 0.9)), 64)
        sphere.setMaterial(m4)
        sphere.renderingRouting = "lighting"
        self.addChild(sphere)

        l0 = Light(Point([0.0, 0, 0.0]), np.array((*ColorType.WHITE, 1.0)))
        lightCube0 = Component(Point((0.0, 0, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"
        self.addChild(lightCube0)

        l1 = Light(Point([0, 0, -3.0]), np.array((*ColorType.SOFTRED, 1.0)), infiniteDirection=Point((0, 0, -1)))
        lightCube1 = Component(Point((0, 0, -3.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTRED))
        lightCube1.renderingRouting = "vertex"
        self.addChild(lightCube1)

        self.lights = [l0, l1]
        self.lightCubes = [lightCube0, lightCube1]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
