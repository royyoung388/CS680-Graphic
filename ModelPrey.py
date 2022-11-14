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


class ModelPrey(Component, EnvironmentObject):
    """
    Define our linkage model
    """

    components = None
    contextParent = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, position, shaderProg, color, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent
        self.components = []
        self.componentDict = {}
        self.rotation_speed = [-1, 1]
        self.translation_speed = 0.02

        self.setDefaultScale([0.3, 0.3, 0.3])

        # boid algorithm
        self.viewRange = 2

        # self.direction = Point((0, 0, 0)) * self.translation_speed
        self.direction = self.randomPoint().normalize() * self.translation_speed
        # bounding
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.15
        self.species_id = 3

        body = Sphere(Point((0, 0, 0)), shaderProg, [.1, .1, 0.5], Ct.GRAY)
        antenna1 = Cylinder(Point((0, 0, 0.5)), shaderProg, [.01, .01, .3], Ct.GRAY)
        antenna1.rotate(10, antenna1.vAxis)
        antenna2 = Cylinder(Point((0, 0, 0.5)), shaderProg, [.01, .01, .3], Ct.GRAY)
        antenna2.rotate(-10, antenna2.vAxis)

        wing1 = Cone((Point((0.25, 0, 0))), shaderProg, [0.3, 0.01, 0.4], color)
        wing1.rotate(-10, wing1.vAxis)
        wing2 = Cone((Point((-0.25, 0, 0))), shaderProg, [0.3, 0.01, 0.4], color)
        wing2.rotate(10, wing2.vAxis)

        wing1.setRotateExtent(wing1.wAxis, -25, 25)
        wing2.setRotateExtent(wing1.wAxis, -25, 25)

        self.addChild(body)
        body.addChild(antenna1)
        body.addChild(antenna2)
        body.addChild(wing1)
        body.addChild(wing2)

        self.components.extend([body, antenna1, antenna2, wing1, wing2])
        self.componentDict.update({'body': body,
                                   'antenna1': antenna1,
                                   'antenna2': antenna2,
                                   'wing1': wing1,
                                   'wing2': wing2})

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create period animation for creature joints
        if self.componentDict['wing1'].wAngle in self.componentDict['wing1'].wRange:
            self.rotation_speed = [f * -1 for f in self.rotation_speed]

        for i, w in enumerate(['wing1', 'wing2']):
            self.componentDict[w].rotate(self.rotation_speed[i], self.componentDict[w].wAxis)

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
        #
        potential = Point((0, 0, 0))
        for c in components:
            # ignore tank
            if c.species_id == -1:
                continue
            dis = (self.currentPos + self.bound_center).distance(c.currentPos + c.bound_center)

            # ModelPredator
            if c.species_id == 2:
                # potential function: repulse ModelPredator
                potential -= 3 * (c.currentPos + c.bound_center - self.currentPos + self.bound_center) * math.exp(
                    -dis ** 2)
            elif c.species_id == 4:
                # food
                if dis <= self.bound_radius + c.bound_radius:
                    # eat food
                    vivarium.delObjInTank(c)
                else:
                    # attractive potential function
                    potential += 0.5 * (c.currentPos + c.bound_center - self.currentPos + self.bound_center) * math.exp(
                        -dis ** 2)
            # elif c.species_id == 3 and c != self:
            # other ModelPrey
            # # no collision
            # if dis > self.bound_radius + c.bound_radius:
            #     continue
            # # collision, bounce back
            # norm = self.direction - c.direction
            # self.direction = self.direction.reflect(norm)
            # c.direction = c.direction.reflect(norm)


        others = [c for c in components if c.species_id == 3 and c != self]
        self.boid_cohesion(others)
        self.boid_separation(others)
        self.boid_alignment(others)
        self.direction += 0.001 * potential

        # limit speed
        if self.direction.norm() > self.translation_speed:
            self.direction = self.direction.normalize() * self.translation_speed
        self.keepInTank(self.currentPos + self.direction, self.direction, tank_dimensions)

        # self.direction = (potential.normalize() + self.direction.normalize()) * self.translation_speed
        # newCenter = self.currentPos + self.direction + self.bound_center
        # self.direction = self.tankCollision(newCenter, self.direction, tank_dimensions)

        self.setQuaternion(self.rotateDirection(Point((0, 0, -1)), self.direction))
        self.setCurrentPosition(self.currentPos + self.direction)

    # find the center of boids, adjust direction slightly to the center
    def boid_cohesion(self, others):
        # change factor
        factor = 0.0005
        center = self.currentPos.copy()
        count = 1

        for boid in others:
            if self.currentPos.distance(boid.currentPos) < self.viewRange:
                center += boid.currentPos
                count += 1

        center = center * (1.0 / count)
        self.direction += (center - self.currentPos) * factor

    # Move away from other boids that are too close to avoid colliding
    def boid_separation(self, others):
        # change factor
        factor = 0.01
        minDistance = 0.5
        escape = Point((0, 0, 0))

        for boid in others:
            if self.currentPos.distance(boid.currentPos) < minDistance:
                escape += self.currentPos - boid.currentPos

        self.direction += escape * factor

    # Find the average velocity (speed and direction) and match velocity
    def boid_alignment(self, others):
        # change factor
        factor = 0.01
        avg = self.direction.copy()
        count = 1

        for boid in others:
            if self.currentPos.distance(boid.currentPos) < self.viewRange:
                avg += boid.direction

        avg = avg * (1.0 / count)
        self.direction += (avg - self.direction) * factor

    # def reset(self, mode="all"):
    #     super().reset(mode)
    #     self.direction = self.randomPoint().normalize() * self.translation_speed
