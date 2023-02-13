"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

import math

import numpy as np

import ColorType
from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO

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


class DisplayableSphere(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radius = None
    color = None
    stacks = None
    slices = None
    texture = False

    def __init__(self, shaderProg, radius=1, stacks=30, slices=30, color=ColorType.BLUE, texture=False):
        super(DisplayableSphere, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, stacks, slices, color, texture)

    def generate(self, radius=1, stacks=30, slices=30, color=None, texture=False):
        self.radius = radius
        self.color = color
        self.stacks = stacks
        self.slices = slices
        self.texture = texture
        pi = math.pi

        self.vertices = np.zeros([(stacks + 1) * (slices + 1), 17])

        # stacks
        for i, phi in enumerate(np.arange(-pi / 2, pi / 2 + pi / stacks, pi / stacks)):
            # slices
            for j, theta in enumerate(np.arange(-pi, pi + 2 * pi / slices, 2 * pi / slices)):
                x = radius * math.cos(phi) * math.cos(theta)
                y = radius * math.cos(phi) * math.sin(theta)
                z = radius * math.sin(phi)

                x_normal = math.cos(phi) * math.cos(theta)
                y_normal = math.cos(phi) * math.sin(theta)
                z_normal = math.sin(phi)

                pu_x = -radius * math.cos(phi) * math.sin(theta)
                pu_y = radius * math.cos(phi) * math.cos(theta)
                pu_z = 0

                pv_x = - radius * math.sin(phi) * math.cos(theta)
                pv_y = - radius * math.sin(phi) * math.sin(theta)
                pv_z = radius * math.cos(phi)

                self.vertices[i * (slices + 1) + j] = [x, y, z, x_normal, y_normal, z_normal, *color, 0, 0,
                                                       pu_x, pu_y, pu_z, pv_x, pv_y, pv_z]

                if texture:
                    self.vertices[i * (slices + 1) + j][9:11] = [1.0 / slices * j,
                                                                 1 - 1.0 / (stacks + 1) * i]

        triangle_list = []
        # stacks
        for i in range(stacks):
            # slices
            for j in range(slices):
                # if j == slices - 1:
                #     triangle_list.extend([
                #         i * slices + j, (i + 1) * slices + j, (i + 1) * slices,
                #         i * slices + j, (i + 1) * slices, i * slices,
                #     ])
                # else:
                triangle_list.extend([
                    i * (slices + 1) + j, (i + 1) * (slices + 1) + j, (i + 1) * (slices + 1) + j + 1,
                    i * (slices + 1) + j, (i + 1) * (slices + 1) + j + 1, i * (slices + 1) + j + 1,
                ])

        self.indices = np.array(triangle_list)

    def draw(self):
        self.vao.bind()
        # self.vbo.draw()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 17)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=17, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=17, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=17, offset=6, attribSize=3)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=17, offset=9, attribSize=2)
        # normal mapping
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPu"),
                                  stride=17, offset=11, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPv"),
                                  stride=17, offset=14, attribSize=3)
        self.vao.unbind()
