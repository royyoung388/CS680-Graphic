#### 1\. Overview

This programming assignment is meant to acquaint you with 3D modeling and model transformation. You will implement a creature model and make it move by performing transformations on its joints. You will also need to submit a simple reference image or concept drawing and a screenshot of your model with your code.

##### Basic Requirements

Before coding, please have a look at the Component class defined in "Component.py". We recommend calling functions of the Component class in your keyboard event functions to make the joints/body of your creature move.

After reading the code in the "Component.py" file, you should start implementing certain features in certain blocks/files in the skeleton code:

1.  TODO 1 in "Component.py": please complete the Component.update() function that sets the transformation matrix of each component. Most of this function has already been written: you only need to provide one line of code that shows the correct multiplication order of the matrices that have already been created for you. Specifically, you need to account for translations, rotations, and scaling in addition to the parent transformation matrix that is passed to this function. There are also pre-rotation and post-rotation matrices used to properly set the position of each component before it is rotated. You can multiply numpy matrices together using the @ operator (e.g. self.transformationMat = C @ B @ A).  
      
    
2.  TODO 2 in "ModelLinkage.py": please implement your own creature class by following the form of the provided ModelLinkage class. You will need to make use of the geometric primitives defined in Shapes.py. Combine these shapes in a hierarchical fashion to construct a sufficiently complex 3D model of a creature (insect, spider, scorpion, etc.) Please see "Model Requirements" for additional details on what is required of your model. You will need to figure out how to store components in a hierarchical structure and set them in proper position by chaining transformations. It is helpful to modularize your design in one class — you may need to reuse your model in future programming assignments.
    
      
      
    
3.  TODO 3 in "Sketch.py": After building your model, you need to create an instance of it in Sketch.py. See the InitGL function.  
      
    
4.  TODO 4 in "Sketch.py" or "ModelLinkage.py": Set up the joint behaviors of your creature. Please refer to the Component class to see what functions are already available to you. Limit the angles at each joint within reasonable ranges so that the creature's legs, neck, head and any other parts don't intersect or bend in unnatural ways! The orientation of joint rotations for the left and right limbs must mirror each other.  
      
    
5.  TODO 5 in "Sketch.py": Set up the keyboard events that make your creature act in different ways (change poses, rotate limbs, etc.). Please add a multi-select feature to the interface, so you can control several joints at the same time. You will need to set up at least 5 different poses for your creature as test cases. Please check your keyboard events and test cases to see if they work as expected and satisfy our requirements.  
      
    
6.  TODO 6 in "Sketch.py" **(Extra Credit for CS480 students)**: Implement an eye that always looks at the position of the mouse when no rotation of the camera is performed. An eye should consist of a movable pupil and still sclera.

##### Extra Credit

7.  Use **quaternions** rather than Euler rotations to implement the eye tracking feature for additional credit.
    

##### Programming Style

For any modified or newly added source file, you should include a brief description of how this file was changed. Add this information to the file heading along with your name and ID. Your code should be readable with sufficient comments. You should use consistent variable naming and keep reasonable indentation.

  

##### README

With each assignment, please upload a README text or markdown file with the following information:

*   your name
*   any collaborators that you spoke to
*   the class
*   the assignment number
*   a brief summary of the code and implementations you have written for the assignment

  

For the last point, you should outline the method you used to solve the problem, describe the variables and data-structures used in the program, any error conditions which might be encountered in the solution, and how these error conditions are handled by the solution.

  

If these details are described in the comments above the relevant functions or files, you may be brief here. You may call this file "READMEStudent" or something analogous to differentiate it from the README in the skeleton code.

**Please include a mention of any resources that you consulted while completing your assignment.**

##### Model Requirements

In addition to roughly following the reference image/drawing you will provide, your model should be suitably complex:

*   at least 6 limbs required (tails and wings count)
*   at least one limb must have at least 3 joints
*   at least two colors should be used
*   at least two shape types must be used
*   a pair of opposing limbs must be present (to test mirrored motions)

#### 2\. Resources

##### 2.1 Starter code

A Python Program skeleton [PA2.zip](https://learn.bu.edu/bbcswebdav/pid-10747830-dt-content-rid-73708156_1/xid-73708156_1), which includes basic classes, methods, and main pipeline, is provided for you. You are expected to complete the sketch program by completing/modifying Sketch.py. There are comments in the skeleton code that will help guide you in writing your own subroutines. Some of them are noted as "TODO" or "BONUS" which suggest you should complete the corresponding block.

##### 2.2 Environment Setup

Installing the appropriate programming environment should be covered in a lab session. For more step-by-step instructions, please check the environment setup page. 

##### 2.3 User Interface

The user interface to the program is provided through mouse buttons and keyboard keys:

*   **ENTER/RETURN**: Cycle through components
*   **LEFT-ARROW, RIGHT-ARROW**: Iterate through different rotation axis for the currently selected component
*   **UP-ARROW**, mouse **SCROLL-UP**: Increase selected component's rotation angle along the selected axis
*   **DOWN-ARROW**, mouse **SCROLL-DOWN**: Decrease selected component's rotation angle along the selected axis
*   mouse **Left-Drag**: change the viewing angle
*   **r**: reset the viewing angle
*   **R**: reset everything in the scene

After modifications, your interface may be different from the example program provided here. Don't forget to add a multi-select feature so multiple joints can be changed simultaneously.

##### 2.4 Demo

We prepare a demo video for you. Even though the "creature" in the video doesn't fully satisfy our requirements, this is still good to show how the multi-select works and what will be like if you set the rotation limit correctly. 

#### 3\. Submission (due by 11:59 PM, Tuesday, 10/18)

##### 3.1 Source Code

Your program's source files are to be submitted electronically on Gradescope. Please wrap everything in your project folder to a zip file and submit it. The code you submit should conform to the program assignment guidelines.

##### 3.2 Demo

Part of your grade for this programming assignment will be based on your giving a short demo (5 minutes) during the CS480/680 scheduled labs following the assignment due date. You will be expected to talk about how your program works.

##### 3.3 Reference image/drawing and screenshot

Please submit a reference image or drawing of your design and a corresponding screenshot. The image/drawing can be relatively simple, and is simply to motivate some modeling with intent.

#### 4\. Grading

Students can receive at maximum 10 points of extra credit.

|**Task**|**CS480**|**CS680**|
|-----|-----|-----|
|3D Creature model constructed satisfies requirements for shapes, hierarchies, and color|25|25|
|Proper rotation at the joints|25|25|
|Limit rotation so that limbs do not bend in unnatural ways|10|10|
|Your predefined 5 creature poses work properly|25|25|
|The creature design is similar to your reference image/drawing|5|5|
|Eye movement|5 (extra)|15|
|Eye movement with quaternions|10 (extra)|10 (extra)|
|Programming style (See Assignments > General Guidelines)|10|10|

#### 5\. Code Distribution Policy

You acknowledge this code is only for the course learning purpose. You should never distribute any part of this assignment, especially the completed version, to any publicly accessible website or open repository without our permission. Keep the code in your local computer or private repository is allowed. You should never share, sell, gift or copy the code in any format with any other person without our permission.