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


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    height = None
    radius = None
    slices = None
    color = None

    def __init__(self, shaderProg, height=1, radius=1, slices=30, color=ColorType.BLUE):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(height, radius, slices, color)

    def generate(self, height=1, radius=1, slices=30, color=None):
        self.height = height
        self.radius = radius
        self.slices = slices
        self.color = color
        pi = math.pi

        self.vertices = np.zeros([slices * 4 + 2, 17])

        # slices
        for i, theta in enumerate(np.arange(-pi, pi, 2 * pi / slices)):
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            z = height / 2

            x_normal = radius * math.cos(theta)
            y_normal = radius * math.sin(theta)
            z_normal = 0

            pu_x = -radius * math.sin(theta)
            pu_y = radius * math.cos(theta)
            pu_z = 0

            # surface: top and bot
            self.vertices[i * 4] = [x, y, z, x_normal, y_normal, z_normal, *color, 0, 0, pu_x, pu_y, pu_z, 0, 0, 1]
            self.vertices[i * 4 + 1] = [x, y, -z, x_normal, y_normal, z_normal, *color, 0, 0, pu_x, pu_y, pu_z, 0,
                                             0, 1]
            # cap: top and bot
            self.vertices[i * 4 + 2] = [x, y, z, 0, 0, 1, *color, 0, 0, 1, 0, 0, 0, 1, 0]
            self.vertices[i * 4 + 3] = [x, y, -z, 0, 0, -1, *color, 0, 0, 1, 0, 0, 0, 1, 0]

        # cap center
        self.vertices[-2] = [0, 0, height / 2, 0, 0, 1, *color, 0, 0, 1, 0, 0, 0, 1, 0]
        self.vertices[-1] = [0, 0, -height / 2, 0, 0, -1, *color, 0, 0, 1, 0, 0, 0, 1, 0]

        triangle_list = []
        #  surface
        for i in range(slices):
            if i == slices - 1:
                triangle_list.extend([
                    4 * i, 4 * i + 1, 1,
                    4 * i, 1, 0
                ])
            else:
                triangle_list.extend([
                    4 * i, 4 * i + 1, 4 * i + 5,
                    4 * i, 4 * i + 5, 4 * i + 4
                ])

        # cap
        top_center = len(self.vertices) - 2
        bot_center = len(self.vertices) - 1
        for i in range(slices):
            if i == slices - 1:
                triangle_list.extend([
                    top_center, 4 * i + 2, 2,
                    bot_center, 3, 4 * i + 3
                ])
            else:
                triangle_list.extend([
                    top_center, 4 * i + 2, 4 * i + 6,
                    bot_center, 4 * i + 7, 4 * i + 3
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
