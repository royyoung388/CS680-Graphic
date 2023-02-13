"""
Define Torus here.
First version in 11/01/2021

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


##### TODO 6/BONUS 6: Texture Mapping
# Requirements:
#   1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns
#   (i.e. the last two columns). Tell OpenGL how to interpret these two columns:
#   you need to set up attribPointer in the Displayable object's initialize method.
#   2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and
#   “./assets/earth.jpg” for the sphere as the texture image.
#   There should be no seams in the resulting texture-mapped model.

class DisplayableTorus(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    # stores current torus's information, read-only
    nsides = 0
    rings = 0
    innerRadius = 0
    outerRadius = 0
    color = None
    texture = False

    vertices = None
    indices = None

    def __init__(self, shaderProg, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE,
                 texture=False):
        super(DisplayableTorus, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(innerRadius, outerRadius, nsides, rings, color, texture)

    def generate(self, innerRadius=0.25, outerRadius=0.5, nsides=36, rings=36, color=ColorType.SOFTBLUE, texture=False):
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.nsides = nsides
        self.rings = rings
        self.color = color
        self.texture = texture
        pi = math.pi

        # we need to pad one more row for both nsides and rings, to assign correct texture coord to them
        self.vertices = np.zeros([(nsides + 1) * (rings + 1), 17])

        # rings
        for i, phi in enumerate(np.arange(-pi, pi + 2 * pi / rings, 2 * pi / rings)):
            # circle / nsides
            for j, theta in enumerate(np.arange(-pi, pi + 2 * pi / nsides, 2 * pi / nsides)):
                x = (outerRadius + innerRadius * math.cos(theta)) * math.cos(phi)
                y = (outerRadius + innerRadius * math.cos(theta)) * math.sin(phi)
                z = innerRadius * math.sin(theta)

                x_normal = math.cos(theta) * math.cos(phi)
                y_normal = math.cos(theta) * math.sin(phi)
                z_normal = math.sin(theta)

                pu_x = - (outerRadius + innerRadius * math.cos(theta)) * math.sin(phi)
                pu_y = (outerRadius + innerRadius * math.cos(theta)) * math.cos(phi)
                pu_z = 0

                pv_x = - innerRadius * math.sin(theta) * math.cos(phi)
                pv_y = - innerRadius * math.sin(theta) * math.sin(phi)
                pv_z = innerRadius * math.cos(theta)

                self.vertices[i * (nsides + 1) + j] = [x, y, z, x_normal, y_normal, z_normal, *color, 0, 0,
                                                       pu_x, pu_y, pu_z, pv_x, pv_y, pv_z]

                if texture:
                    self.vertices[i * (nsides + 1) + j][9:11] = [1 / rings * i, 1 - 1 / nsides * j]

        triangle_list = []
        # rings
        for i in range(rings):
            # nsides
            for j in range(nsides):
                v1 = i * (nsides + 1) + j
                v2 = i * (nsides + 1) + j + 1
                v3 = (i + 1) * (nsides + 1) + j
                v4 = (i + 1) * (nsides + 1) + j + 1

                # if i == rings - 1 and j == nsides - 1:
                #     v2 = i * nsides
                #     v3 = j
                #     v4 = 0
                # elif j == nsides - 1:
                #     v2 = i * nsides
                #     v4 = (i + 1) * nsides
                # elif i == rings - 1:
                #     v3 = j
                #     v4 = j + 1

                triangle_list.extend([
                    v1, v2, v3,
                    v2, v4, v3
                ])

        self.indices = np.array(triangle_list)

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems which don't enable a default VAO after GLProgram compilation
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
