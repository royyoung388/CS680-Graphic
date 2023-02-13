"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import ColorType
import GLUtility
from Animation import Animation
from Component import Component
from DisplayableCube import DisplayableCube
from DisplayableCylinder import DisplayableCylinder
from DisplayableSphere import DisplayableSphere
from DisplayableTorus import DisplayableTorus
from Light import Light
from Material import Material
from Point import Point
from SceneBase import SceneBase


class SceneThree(Component, Animation, SceneBase):
    lights = None
    lightCubes = None
    shaderProg = None
    glutility = None

    lRadius = None
    lAngles = None
    lTransformations = None

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        self.lTransformations = [self.glutility.translate(0, 2, 0, False),
                                 self.glutility.rotate(60, [0, 0, 1], False),
                                 self.glutility.rotate(120, [0, 0, 1], False)]
        self.lRadius = 3
        self.lAngles = [0, 0, 0]

        sphere = Component(Point((-1, 0, 0)), DisplayableSphere(shaderProg, 1.0, texture=True))
        sphere.setTexture(shaderProg, "./assets/earth.jpg")
        sphere.setNormal(shaderProg, "./assets/normalmap.jpg")
        m1 = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 64)
        sphere.setMaterial(m1)
        sphere.renderingRouting = "nmap texture lighting"
        self.addChild(sphere)

        torus = Component(Point((1, 0, 0)), DisplayableTorus(shaderProg, 0.25, 0.5, 36, 36, texture=True))
        torus.setTexture(shaderProg, "./assets/earth.jpg")
        m2 = Material(np.array((0.01, 0.01, 0.01, 0.01)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0, 0, 0, 1.0)), 64)
        torus.setMaterial(m2)
        torus.renderingRouting = "lighting"
        torus.rotate(90, torus.uAxis)
        self.addChild(torus)

        cylinder = Component(Point((1, 0, 0)), DisplayableCylinder(shaderProg, 1, 0.2))
        m3 = Material(np.array((0.3, 0.3, 0.3, 0.3)), np.array((0.2, 0.2, 0.2, 1)),
                      np.array((0.2, 0.2, 0.2, 1.0)), 32)
        cylinder.setMaterial(m3)
        cylinder.renderingRouting = "lighting"
        cylinder.rotate(90, cylinder.uAxis)
        self.addChild(cylinder)

        # point light
        l0 = Light(self.lightPos(self.lRadius, self.lAngles[0], self.lTransformations[0]),
                   np.array((*ColorType.SOFTRED, 1.0)))
        lightCube0 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTRED))
        lightCube0.renderingRouting = "vertex"
        # point light
        l1 = Light(self.lightPos(self.lRadius, self.lAngles[1], self.lTransformations[1]),
                   np.array((*ColorType.SOFTBLUE, 1.0)))
        lightCube1 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.SOFTBLUE))
        lightCube1.renderingRouting = "vertex"
        # spot light
        l2 = Light(self.lightPos(self.lRadius, self.lAngles[2], self.lTransformations[2]),
                   np.array((*ColorType.WHITE, 1.0)), spotDirection=Point((0, 0, 1)),
                   spotRadialFactor=np.array((1, 1, 0.1)), spotAngleFactor=4, spotAngleLimit=15)
        lightCube2 = Component(Point((0, 0, 0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube2.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.addChild(lightCube1)
        self.addChild(lightCube2)
        self.lights = [l0, l1, l2]
        self.lightCubes = [lightCube0, lightCube1, lightCube2]

    def lightPos(self, radius, thetaAng, transformationMatrix):
        r = np.zeros(4)
        r[0] = radius * math.cos(thetaAng / 180 * math.pi)
        r[2] = radius * math.sin(thetaAng / 180 * math.pi)
        r[3] = 1
        r = transformationMatrix @ r
        return r[0:3]

    def animationUpdate(self):
        self.lAngles[0] = (self.lAngles[0] + 0.5) % 360
        self.lAngles[1] = (self.lAngles[1] + 0.7) % 360
        self.lAngles[2] = (self.lAngles[2] + 1.0) % 360
        for i, v in enumerate(self.lights):
            lPos = self.lightPos(self.lRadius, self.lAngles[i], self.lTransformations[i])
            self.lightCubes[i].setCurrentPosition(Point(lPos))
            self.lights[i].setPosition(lPos)
            if self.lights[i].spotOn:
                self.lights[i].setSpotDirection(-1 * Point(lPos).normalize())
            self.shaderProg.setLight(i, v)

        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
