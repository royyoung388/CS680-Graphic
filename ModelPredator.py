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


class ModelPredator(Component, EnvironmentObject):
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
        self.rotation_speed = [-1, 1, 1]
        self.translation_speed = 0.01

        self.setDefaultScale([0.3, 0.3, 0.3])

        self.direction = Point((0, 0, 0)) * self.translation_speed
        # bounding
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.3
        self.species_id = 2

        body = Sphere(Point((0, 0, 0)), shaderProg, [0.5, 0.3, 0.7], Ct.SEAGREEN)
        head = Sphere(Point((0, 0, 0.7)), shaderProg, [0.3, 0.2, 0.2], Ct.GREENYELLOW)
        # head angle
        # head.setRotateExtent(head.uAxis, -90, 90)
        # head.setRotateExtent(head.vAxis, -90, 90)
        # head.setRotateExtent(head.wAxis, -90, 90)

        # eye
        eye1 = self.eye(Point((-0.1, 0, 0.18)), shaderProg, 'eye1')
        eye2 = self.eye(Point((0.1, 0, 0.18)), shaderProg, 'eye2')

        # leg
        leg1 = self.leg(Point((0.4, 0, 0.15)), shaderProg, 'leg1', 90)
        leg2 = self.leg(Point((-0.4, 0, 0.15)), shaderProg, 'leg2', -90)
        leg3 = self.leg(Point((0.4, 0, 0.45)), shaderProg, 'leg3', 70)
        leg4 = self.leg(Point((-0.4, 0, 0.45)), shaderProg, 'leg4', -70)
        leg5 = self.leg(Point((0.4, 0, -0.15)), shaderProg, 'leg5', 110)
        leg6 = self.leg(Point((-0.4, 0, -0.15)), shaderProg, 'leg6', -110)

        # teeth
        teeth1 = Cone(Point((-0.1, -0.1, 0.2)), shaderProg, [0.05, 0.05, 0.1], Ct.ORANGE)
        # angle
        teeth1.setDefaultAngle(40, teeth1.uAxis)
        teeth1.setDefaultAngle(20, teeth1.wAxis)
        teeth1.setRotateExtent(teeth1.uAxis, 40, 40)
        teeth1.setRotateExtent(teeth1.vAxis, -40, 30)
        teeth1.setRotateExtent(teeth1.wAxis, 20, 20)
        teeth2 = Cone(Point((0.1, -0.1, 0.2)), shaderProg, [0.05, 0.05, 0.1], Ct.ORANGE)
        # angle
        teeth2.setDefaultAngle(40, teeth2.uAxis)
        teeth2.setDefaultAngle(-20, teeth2.wAxis)
        teeth2.setRotateExtent(teeth2.uAxis, 40, 40)
        teeth2.setRotateExtent(teeth2.vAxis, -30, 40)
        teeth2.setRotateExtent(teeth2.wAxis, -20, -20)

        self.addChild(body)
        body.addChild(head)
        head.addChild(eye1)
        head.addChild(eye2)
        body.addChild(leg1)
        body.addChild(leg2)
        body.addChild(leg3)
        body.addChild(leg4)
        body.addChild(leg5)
        body.addChild(leg6)
        head.addChild(teeth1)
        head.addChild(teeth2)

        self.components.extend([body, head, teeth1, teeth2])
        self.componentDict.update({
            'body': body,
            'head': head,
            'teeth1': teeth1,
            'teeth2': teeth2
        })

    def leg(self, position, shaderProg, name, vAngle):
        leg_length = 0.15
        leg_radius = 0.08
        leg1 = Cylinder(position.copy(), shaderProg, [leg_radius, leg_radius, leg_length], Ct.YELLOW)
        leg2 = Cylinder(Point((0, 0, 2 * leg_length)), shaderProg, [leg_radius, leg_radius, leg_length], Ct.DEEPSKYBLUE)
        leg3 = Cylinder(Point((0, 0, 2 * leg_length)), shaderProg, [leg_radius, leg_radius, leg_length], Ct.YELLOW)
        leg1.setDefaultAngle(vAngle, leg1.vAxis)
        for l in [leg1, leg2, leg3]:
            l.setDefaultAngle(20, l.uAxis)
        leg1.setRotateExtent(leg1.uAxis, -60, 60)
        leg1.setRotateExtent(leg1.vAxis, vAngle - 15, vAngle + 15)
        leg1.setRotateExtent(leg1.wAxis, 0, 0)
        leg2.setRotateExtent(leg2.uAxis, 0, 60)
        leg2.setRotateExtent(leg2.vAxis, 0, 0)
        leg2.setRotateExtent(leg2.wAxis, 0, 0)
        leg3.setRotateExtent(leg3.uAxis, 0, 60)
        leg3.setRotateExtent(leg3.vAxis, 0, 0)
        leg3.setRotateExtent(leg3.wAxis, 0, 0)

        leg1.addChild(leg2)
        leg2.addChild(leg3)

        self.components.extend([leg1, leg2, leg3])
        self.componentDict.update({name + '1': leg1, name + '2': leg2, name + '3': leg3})
        return leg1

    def eye(self, position, shaderProg, name):
        eye_size = 0.05
        eye = Sphere(position.copy(), shaderProg, [eye_size, eye_size, eye_size], Ct.BLACK, False)
        pupil_size = 0.02
        pupil = Sphere(Point((0, 0, eye_size)), shaderProg, [pupil_size, pupil_size, pupil_size], Ct.WHITE)
        eye.addChild(pupil)

        eye.setRotateExtent(eye.uAxis, -45, 45)
        eye.setRotateExtent(eye.vAxis, -45, 45)
        eye.setRotateExtent(eye.wAxis, 0, 0)

        self.components.append(eye)
        self.componentDict.update({name: eye})
        return eye

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create period animation for creature joints
        legs = [[('leg11', 1), ('leg12', 0.5), ('leg13', 0.5), ('leg21', 1), ('leg22', 0.5), ('leg23', 0.5)],
                [('leg31', 1), ('leg32', 0.5), ('leg33', 0.5), ('leg41', 1), ('leg42', 0.5), ('leg43', 0.5)],
                [('leg51', 1), ('leg52', 0.5), ('leg53', 0.5), ('leg61', 1), ('leg62', 0.5), ('leg63', 0.5)]]
        if self.componentDict[legs[0][0][0]].vAngle in self.componentDict[legs[0][0][0]].vRange:
            self.rotation_speed = [f * -1 for f in self.rotation_speed]
        for i, l in enumerate(legs):
            for name, angle in l:
                self.componentDict[name].rotate(self.rotation_speed[i] * angle,
                                                self.componentDict[name].vAxis)

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):
        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between it and tank walls. When it hits with tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.
        potential = Point((0, 0, 0))
        for c in components:
            # chase ModelPrey
            if c.species_id != 3:
                continue
            dis = (self.currentPos + self.bound_center).distance(c.currentPos + c.bound_center)
            # collision -> eat prey
            if dis < self.bound_radius + c.bound_radius:
                vivarium.delObjInTank(c)
            else:
                # potential function
                potential += 2 * (c.currentPos + c.bound_center - self.currentPos + self.bound_center) * math.exp(
                    -dis ** 2)

        # self.direction = (potential.normalize() + self.direction.normalize()) * self.translation_speed
        # newCenter = self.currentPos + self.direction + self.bound_center
        # self.tankCollision(newCenter, self.direction, tank_dimensions)

        self.direction += 0.005 * potential
        # limit speed
        if self.direction.norm() > self.translation_speed:
            self.direction = self.direction.normalize() * self.translation_speed
        self.keepInTank(self.currentPos + self.direction, self.direction, tank_dimensions)

        self.setPostRotation(self.rotateDirection(Point((0, 0, 1)), self.direction).toMatrix())
        self.setCurrentPosition(self.currentPos + self.direction)

    # def reset(self, mode="all"):
    #     super().reset(mode)
    #     self.direction = Point((0, 0, 0))
