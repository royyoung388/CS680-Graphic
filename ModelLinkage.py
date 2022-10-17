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

import ColorType as Ct
from Point import Point
from Shapes import *


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent
        self.componentList = []
        self.componentDict = {}

        ##### TODO 4: Define creature's joint behavior
        body = Sphere(Point((0, 0, 0)), shaderProg, [0.5, 0.3, 0.7], Ct.SEAGREEN)
        head = Sphere(Point((0, 0, 0.7)), shaderProg, [0.3, 0.2, 0.2], Ct.GREENYELLOW)
        # head angle
        head.setRotateExtent(head.uAxis, -45, 45)
        head.setRotateExtent(head.vAxis, -45, 45)
        head.setRotateExtent(head.wAxis, -60, 60)

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

        self.componentList.extend([body, head, teeth1, teeth2])
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

        self.componentList.extend([leg1, leg2, leg3])
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

        self.componentList.append(eye)
        self.componentDict.update({name: eye})
        return eye
