'''
Define Our class which is stores collision detection and environment information here
Created on Nov 1, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener 08/2022
'''

import math
import random

from Point import Point
from Quaternion import Quaternion


class EnvironmentObject:
    """
    Define properties and interface for a object in our environment
    """
    env_obj_list = None  # list<Environment>
    item_id = 0
    species_id = 0

    bound_radius = None
    bound_center = Point((0, 0, 0))

    def addCollisionObj(self, a):
        """
        Add an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.append(a)

    def rmCollisionObj(self, a):
        """
        Remove an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.remove(a)

    def animationUpdate(self):
        """
        Perform the next frame of this environment object's animation.
        """
        self.update()

    def stepForward(self):
        """
        Have this environment object take a step forward in the simulation.
        """
        return

    ##### TODO 4: Eyes on the road!
    # Requirements:
    #   1. Creatures should face in the direction they are moving. For instance, a fish should be facing the
    #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
    #   so they should be able to face any direction in 3D space.
    def rotateDirection(self, v1, v2):
        """
        change this environment object's orientation from v1 to v2.
        :param v1: current facing direction
        :type v1: Point
        :param v2: targeted facing direction
        :type v2: Point
        """
        pivot = v1.cross3d(v2).normalize()
        angle = math.acos(round(v1.dot(v2) / v1.norm() / v2.norm(), 2))
        pivot = pivot * math.sin(angle / 2)
        return Quaternion(math.cos(angle / 2), *pivot)

    def tankCollision(self, newCenter, direction, tank_dimensions):
        """
        detect tank collision
        """
        # tank x aix collision
        if abs(newCenter[0] - tank_dimensions[0] / 2) < self.bound_radius \
                or abs(newCenter[0] + tank_dimensions[0] / 2) < self.bound_radius:
            direction.coords[0] = -direction[0]
        # tank y aix collision
        if abs(newCenter[1] - tank_dimensions[1] / 2) < self.bound_radius \
                or abs(newCenter[1] + tank_dimensions[1] / 2) < self.bound_radius:
            direction.coords[1] = -direction[1]
        # tank z aix collision
        if abs(newCenter[2] - tank_dimensions[2] / 2) < self.bound_radius \
                or abs(newCenter[2] + tank_dimensions[2] / 2) < self.bound_radius:
            direction.coords[2] = -direction[2]

        return direction

    def keepInTank(self, newCenter, direction, tank_dimensions):
        """
        constraint creatures in tank. If it's close to edge, nudge it back
        """
        margin = 0.0
        turnFactor = 0.005
        # tank x aix
        if abs(newCenter[0] - tank_dimensions[0] / 2) < self.bound_radius + margin \
                or abs(newCenter[0] + tank_dimensions[0] / 2) < self.bound_radius + margin:
            direction.coords[0] -= abs(newCenter[0]) / newCenter[0] * turnFactor
        # tank y aix
        if abs(newCenter[1] - tank_dimensions[1] / 2) < self.bound_radius + margin \
                or abs(newCenter[1] + tank_dimensions[1] / 2) < self.bound_radius + margin:
            direction.coords[1] -= abs(newCenter[1]) / newCenter[1] * turnFactor
        # tank z aix
        if abs(newCenter[2] - tank_dimensions[2] / 2) < self.bound_radius + margin \
                or abs(newCenter[2] + tank_dimensions[2] / 2) < self.bound_radius + margin:
            direction.coords[2] -= abs(newCenter[2]) / newCenter[2] * turnFactor

        return direction

    def randomPoint(self):
        """
        generate random point. range [-1, 1]
        """
        x = (random.random() - 0.5) * 2
        y = (random.random() - 0.5) * 2
        z = (random.random() - 0.5) * 2
        return Point((x, y, z))
