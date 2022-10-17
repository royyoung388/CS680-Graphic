"""
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

Modified by Daniel Scrivener 07/2022
"""

import math

import numpy as np

import ColorType
import GLUtility
import Pose
from CanvasBase import CanvasBase
from GLProgram import GLProgram
from ModelAxes import ModelAxes
from ModelLinkage import ModelLinkage
from Point import Point
from Quaternion import Quaternion

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
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


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging

        
    Method Instruction:
        
        
    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
        
    Here are some public variables in parent class you might need:
        
        
    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    last_mouse_middlePosition = None
    components = None

    texture = None
    shaderProg = None
    glutility = None

    lookAtPt = None
    upVector = None
    backgroundColor = None
    # use these three to control camera position, mainly used in mouse dragging
    cameraDis = None
    cameraTheta = None  # theta on horizontal sphere cut, in range [0, 2pi]
    cameraPhi = None  # in range [-pi, pi], for smooth purpose

    viewMat = None
    perspMat = None

    select_obj_index = -1  # index of selected component in self.components
    select_axis_index = -1  # index of selected axis
    select_color = [ColorType.ColorType(1, 0, 0), ColorType.ColorType(0, 1, 0), ColorType.ColorType(0, 0, 1)]

    def __init__(self, parent):
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]
        self.last_mouse_middlePosition = [0, 0]
        self.backgroundColor = ColorType.BLUEGREEN

        # add components to top level
        self.resetView()

        self.glutility = GLUtility.GLUtility()

        # pose index
        self.curPose = -1

    def resetView(self):
        self.lookAtPt = [0, 0, 0]
        self.upVector = [0, 1, 0]
        self.cameraDis = 6
        self.cameraPhi = math.pi / 6
        self.cameraTheta = math.pi / 2

    def InitGL(self):
        """
        Called once in order to initialize the OpenGL environemnt.
        You must set your model here (and not in __init__)
        due to the fact that the shader is only compiled once we reach this function.
        """
        self.shaderProg = GLProgram()
        self.shaderProg.compile()

        ##### TODO 3: Initialize your model
        # You should initialize your model here.
        # self.topLevelComponent should refer to your model
        # and self.components should refer to your model's components.
        # Optionally, you can create a dictionary (self.cDict) to index your model's components by name.

        model = ModelLinkage(self, Point((0, 0, 0)), self.shaderProg)
        axes = ModelAxes(self, Point((-1, -1, -1)), self.shaderProg)

        self.topLevelComponent.clear()
        self.topLevelComponent.addChild(model)
        self.topLevelComponent.addChild(axes)
        self.topLevelComponent.initialize()

        self.components = model.componentList
        self.cDict = model.componentDict

        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClearDepth(1.0)
        gl.glViewport(0, 0, self.size[0], self.size[1])

        # enable depth checking
        gl.glEnable(gl.GL_DEPTH_TEST)

        # set basic viewing matrix
        self.perspMat = self.glutility.perspective(45, self.size.width, self.size.height, 0.01, 100)
        self.shaderProg.setMat4("projectionMat", self.perspMat)
        self.shaderProg.setMat4("viewMat", self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector))
        self.shaderProg.setMat4("modelMat", np.identity(4))

    def getCameraPos(self):
        ct = math.cos(self.cameraTheta)
        st = math.sin(self.cameraTheta)
        cp = math.cos(self.cameraPhi)
        sp = math.sin(self.cameraPhi)
        result = [self.lookAtPt[0] + self.cameraDis * ct * cp,
                  self.lookAtPt[1] + self.cameraDis * sp,
                  self.lookAtPt[2] + self.cameraDis * st * cp]
        return result

    def OnResize(self, event):
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)
        self.size = self.GetClientSize()
        self.size[1] = max(1, self.size[1])  # avoid divided by 0
        self.SetCurrent(self.context)

        self.init = False
        self.Refresh(eraseBackground=True)
        self.Update()

    def OnPaint(self, event=None):
        """
        This will be called at every frame
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Init the OpenGL environment if not initialized
            self.InitGL()
            self.init = True
        # the draw methods
        self.OnDraw()

    def OnDraw(self):
        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # These are per-frame updates to the shader. Update the viewing matrix
        self.viewMat = self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector)
        self.shaderProg.setMat4("viewMat", self.viewMat)

        self.topLevelComponent.update(np.identity(4))
        self.topLevelComponent.draw(self.shaderProg)

        self.SwapBuffers()

    def OnDestroy(self, event):
        """
        Window destroy event binding

        :param event: Window destroy event
        :return: None
        """
        if self.shaderProg is not None:
            del self.shaderProg
        super(Sketch, self).OnDestroy(event)

    def Interrupt_MouseMoving(self, x, y):
        ##### TODO 6 (Extra credit for CS480): Eye movement
        # Make your creature's eyes follow the cursor.
        # Try to implement this using quaternions!
        mouse = self.unprojectCanvas(x, y, 0.1)
        mouse[2] = self.cameraDis
        # print('mouse', mouse)

        # # for simplicity, treat eye as origin point
        # # eye direction is [0, 0, 1]
        # angle_u = -math.degrees(math.atan(mouse[1] / mouse[2]))
        # print('angle_u', angle_u)
        # angle_v = math.degrees(math.atan(mouse[0] / mouse[2]))
        # print('angle_v', angle_v)
        # self.cDict['eye1'].rotate(angle_u, self.cDict['eye1'].uAxis)
        # self.cDict['eye1'].rotate(angle_v, self.cDict['eye1'].vAxis)
        # self.cDict['eye2'].rotate(angle_u, self.cDict['eye2'].uAxis)
        # self.cDict['eye2'].rotate(angle_v, self.cDict['eye2'].vAxis)

        # quaternions
        # pivot: (1, 0, 0)
        theta_half = math.atan(mouse[1] / mouse[2]) / 2
        quat_u = Quaternion(math.cos(theta_half), v0=math.sin(theta_half))
        # pivot: (0, 1, 0)
        theta_half = -math.atan(mouse[0] / mouse[2])
        quat_v = Quaternion(math.cos(theta_half), v1=math.sin(theta_half))
        # rotation
        self.cDict['eye1'].setQuaternion(quat_u.multiply(quat_v))
        self.cDict['eye2'].setQuaternion(quat_u.multiply(quat_v))

    def Interrupt_Scroll(self, wheelRotation):
        """
        When mouse wheel rotating detected, do following things

        :param wheelRotation: mouse wheel changes, normally +120 or -120
        :return: None
        """
        if wheelRotation == 0:
            return
        wheelChange = wheelRotation / abs(wheelRotation)  # normalize wheel change
        # rotate multi object
        if isinstance(self.select_obj_index, list) and len(self.components) > 0:
            for l in self.select_obj_index:
                for name, angle in l:
                    self.cDict[name].rotate(wheelChange * 5 * angle,
                                            self.cDict[name].axisBucket[self.select_axis_index])
        # rotate single object
        else:
            if len(self.components) > 0 and self.select_obj_index >= 0:
                self.components[self.select_obj_index].rotate(wheelChange * 5,
                                                              self.components[self.select_obj_index].
                                                              axisBucket[self.select_axis_index])
        self.update()

    def unprojectCanvas(self, x, y, u=0.5):
        """
        unproject a canvas point to world coordiantes. 2D -> 3D
        you need give an extra parameter u, to tell the method how far are you from znear
        u is the proportion of distance to znear / zfar-znear
        in the gluUnProject, the distribution of z is not linear when using perspective projection,
        so z=0.5 is not in the middle,
        that's why we compute out the ray and use linear interpolation and u to get the point

        :param u: u is the proportion to the znear/, in range [0, 1]
        :type u: float
        """
        result1 = glu.gluUnProject(x, y, 0.0,
                                   np.identity(4),
                                   self.viewMat @ self.perspMat,
                                   gl.glGetIntegerv(gl.GL_VIEWPORT))
        result2 = glu.gluUnProject(x, y, 1.0,
                                   np.identity(4),
                                   self.viewMat @ self.perspMat,
                                   # be careful, the concate of view and persp is called projection matrix in opengl
                                   gl.glGetIntegerv(gl.GL_VIEWPORT))
        result = Point([(1 - u) * r1 + u * r2 for r1, r2 in zip(result1, result2)])
        return result

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseMiddleDragging(self, x, y):
        """
        When mouse drag motion with middle key detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """
        dx = x - self.last_mouse_middlePosition[0]
        dy = y - self.last_mouse_middlePosition[1]

        originalMidPt = self.unprojectCanvas(*self.last_mouse_middlePosition, 0.5)

        # ignore sudden change
        self.last_mouse_middlePosition[0] = x
        self.last_mouse_middlePosition[1] = y
        if dx * dx + dy * dy > 5:
            return

        currentMidPt = self.unprojectCanvas(x, y, 0.5)
        changes = currentMidPt - originalMidPt
        moveSpeed = 0.185 * self.cameraDis / 6
        self.lookAtPt = [self.lookAtPt[0] - changes[0] * moveSpeed,
                         self.lookAtPt[1] - changes[1] * moveSpeed,
                         self.lookAtPt[2] - changes[2] * moveSpeed]

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """
        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]

        # ignore sudden change
        if dx * dx + dy * dy > 5:
            self.last_mouse_leftPosition[0] = x
            self.last_mouse_leftPosition[1] = y
            return

        # restrict phi movement range, stop cameraphi changes at pole points
        self.cameraPhi = min(math.pi / 2, max(-math.pi / 2, self.cameraPhi - dy / 100))
        self.cameraTheta += dx / 100

        self.cameraPhi = (self.cameraPhi + math.pi) % (2 * math.pi) - math.pi
        self.cameraTheta = self.cameraTheta % (2 * math.pi)

        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.topLevelComponent.update(np.identity(4))

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """

        ##### TODO 5: Set up your poses and finish the user interface
        # Define keyboard events to make your creature act in different ways when keys are pressed.
        # Create five unique poses to demonstrate your creature's joint rotations.
        # HINT: selecting individual components is easier if you create a dictionary of components (self.cDict)
        # that can be indexed by name (e.g. self.cDict["leg1"] instead of self.components[10])

        if keycode in [wx.WXK_RETURN]:
            # enter component editing mode

            self.select_axis_index = 0

            # reset selected objects and index
            if isinstance(self.select_obj_index, list):
                for l in self.select_obj_index:
                    for name, _ in l:
                        self.cDict[name].reset('color')
                self.select_obj_index = -1

            if len(self.components) > 0:
                # reset color of last selected component
                self.components[self.select_obj_index].reset("color")
                # set new selected component & its color
                self.select_obj_index = (self.select_obj_index + 1) % len(self.components)
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])

            self.update()
        if keycode in [wx.WXK_LEFT]:
            # Last rotation axis of this component
            self.select_axis_index = (self.select_axis_index - 1) % 3
            if isinstance(self.select_obj_index, int) and self.select_obj_index >= 0:
                # single select
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            else:
                # multi select
                for l in self.select_obj_index:
                    for name, _ in l:
                        self.cDict[name].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_RIGHT]:
            # Next rotation axis of this component
            self.select_axis_index = (self.select_axis_index + 1) % 3
            if isinstance(self.select_obj_index, int) and self.select_obj_index >= 0:
                # single select
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
            else:
                # multi select
                for l in self.select_obj_index:
                    for name, _ in l:
                        self.cDict[name].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_UP]:
            # Increase rotation angle
            self.Interrupt_Scroll(1)
            self.update()
        if keycode in [wx.WXK_DOWN]:
            # Decrease rotation angle
            self.Interrupt_Scroll(-1)
            self.update()
        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            self.components[self.select_obj_index].reset("color")
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()
        if chr(keycode) in "r":
            # reset viewing angle only
            self.resetView()
        if chr(keycode) in "R":
            # reset everything
            for c in self.components:
                c.reset()
            self.resetView()
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()
        # show rotation angle for each object
        # used to design poses
        if chr(keycode) in 's':
            for name, obj in self.cDict.items():
                print("'%s': (%d, %d, %d)," % (name, obj.uAngle, obj.vAngle, obj.wAngle))
            print()
        # switch pose
        if chr(keycode) in 'p':
            # update pose index
            self.curPose = self.curPose + 1
            self.curPose %= len(Pose.pose)
            # reset object
            for c in self.components:
                c.reset()
            self.select_obj_index = -1
            self.select_axis_index = -1
            # show pose
            for name, angle in Pose.pose[self.curPose].items():
                obj = self.cDict[name]
                obj.setCurrentAngle(angle[0], obj.uAxis)
                obj.setCurrentAngle(angle[1], obj.vAxis)
                obj.setCurrentAngle(angle[2], obj.wAxis)
            self.update()
        # number select
        action = {'1': [('leg11', 1), ('leg12', 0.5), ('leg13', 0.5), ('leg21', 1), ('leg22', 0.5), ('leg23', 0.5)],
                  '2': [('leg31', 1), ('leg32', 0.5), ('leg33', 0.5), ('leg41', 1), ('leg42', 0.5), ('leg43', 0.5)],
                  '3': [('leg51', 1), ('leg52', 0.5), ('leg53', 0.5), ('leg61', 1), ('leg62', 0.5), ('leg63', 0.5)],
                  '4': [('body', 1)],
                  '5': [('head', 1)],
                  '6': [('eye1', 1), ('eye2', 1)],
                  '7': [('teeth1', 1), ('teeth2', -1)]}
        number = chr(keycode)
        # rotate legs
        if number in action:
            # first case
            if not isinstance(self.select_obj_index, list):
                # reset color
                self.components[self.select_obj_index].reset("color")
                self.select_axis_index = 0
                self.select_obj_index = [action[number]]
            # selected, then remove and reset
            elif action[number] in self.select_obj_index:
                self.select_obj_index.remove(action[number])
                for name, _ in action[number]:
                    self.cDict[name].reset('color')
            # not selected, add to list
            else:
                self.select_obj_index.append(action[number])

            # set color for selected objects
            for l in self.select_obj_index:
                for name, _ in l:
                    self.cDict[name].setCurrentColor(self.select_color[self.select_axis_index])

            self.update()


if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
