"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener
"""
import random

import ColorType
from Component import Component
from EnvironmentObject import EnvironmentObject
from ModelFood import ModelFood
from ModelPredator import ModelPredator
from ModelPrey import ModelPrey
from ModelTank import Tank
from Point import Point


class Vivarium(Component):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent, shaderProg):
        self.parent = parent
        self.shaderProg = shaderProg

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(Point((0, 0, 0)), shaderProg, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]
        for c in self.genCreatures():
            self.addNewObjInTank(c)

    def genCreatures(self):
        # self.addNewObjInTank(Linkage(parent, Point((0,0,0)), shaderProg))
        return [ModelPredator(self.parent, Point((0, 0, 0)), self.shaderProg),
                ModelPrey(self.parent, Point((1, 1, 1)), self.shaderProg, ColorType.GREEN),
                ModelPrey(self.parent, Point((-1, 1, 1)), self.shaderProg, ColorType.RED),
                ModelPrey(self.parent, Point((1, -1, 1)), self.shaderProg, ColorType.BLUE),
                ModelPrey(self.parent, Point((1, 1, -1)), self.shaderProg, ColorType.DARKGREEN),
                ModelPrey(self.parent, Point((-1, -1, 1)), self.shaderProg, ColorType.WHITE),
                ModelPrey(self.parent, Point((1, -1, -1)), self.shaderProg, ColorType.GREENYELLOW),
                ModelPrey(self.parent, Point((-1, 1, -1)), self.shaderProg, ColorType.CYAN)]

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """

        for c in self.components[::-1]:
            if isinstance(c, EnvironmentObject):
                c.animationUpdate()
                c.stepForward(self.components, self.tank_dimensions, self)

        self.update()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components

    def genFood(self):
        """
        generate food
        """
        for i in range(5):
            p = self.randomPoint()
            p.coords[1] = self.tank_dimensions[1] / 2 - 0.2
            food = ModelFood(self.parent, p, self.shaderProg)
            food.initialize()
            self.addNewObjInTank(food)

    def randomPoint(self):
        x = (random.random() - 0.5) * self.tank_dimensions[0] / 2
        y = (random.random() - 0.5) * self.tank_dimensions[1] / 2
        z = (random.random() - 0.5) * self.tank_dimensions[2] / 2
        return Point((x, y, z))

    def reset(self):
        """
        reset everything
        """
        # remove all components except tank
        for i in range(len(self.components) - 1, -1, -1):
            c = self.components[i]
            # remove food, predator and prey
            if c.species_id in [2, 3, 4]:
                self.delObjInTank(c)

        for c in self.genCreatures():
            c.initialize()
            self.addNewObjInTank(c)
