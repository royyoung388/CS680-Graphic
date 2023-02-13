# Programming Assignment 04: Shaded Rendering
Name: Pengchao Yuan  
Class: CS680  
Assignment: PA4

## 1. Overview

In this assignment you will use OpenGL Shading Language(GLSL) to write your own vertex and fragment shaders to compute illumination and shading of meshes.

### Basic Requirements
1. **Generate Triangle Meshes (TODO 1):**
    1. Use Element Buffer Object (EBO) to draw the cube. The cube provided in the start code is drawn with Vertex Buffer Object (VBO). In the DisplayableCube class draw method, you should switch from VBO draw to EBO draw. To achieve this, please first read through VBO and EBO classes in GLBuffer. Then you rewrite the self.vertices and self.indices in the DisplayableCube class. Once you have all these down, then switch the line vbo.draw() to ebo.draw().
    2. Generate Displayable classes for an ellipsoid, torus, and cylinder with end caps. These classes should be like the DisplayableCube class and they should all use EBO in the draw method. \
>PS: You must use the ellipsoid formula to generate it, scaling the Displayable sphere doesn't count

Calculate vertices, normal, texture coor and local basis (Pu, Pv).  
Size of vertex is 17 (3 position, 3 normal, 3 color, 2 texture coor, 3 Pu, 3 Pv)
Cube: faces don't share vertices, since different face have different normal and local basis.
Sphere: Use spherical coordinate system to calculate sphere vertices. Slices and stacks will affect the number of vertices.   
Cylinder: Use polar coordinate system to calculate vertices. Bases and surface don't share vertices, since they have different normal and local basis.  
Torus: Use nested polar coordinate system to calculate vertices.

2. **Set Normal Rendering (TODO 2):** As a visual debugging mode, you’ll implement a rendering mode that visualizes the vertex normals with color information. In Fragment Shader, use the vertex normal as the vertex color (i.e. the rgb values come from the xyz components of the normal). The value for each dimension in vertex normal will be in the range -1 to 1. You will need to offset and rescale them to the range 0 to 1.  
Map range for each dimension in normal from [-1, 1] to [0, 1], then set it as color.  

4. **Illuminate your meshes (TODO 3):** Use the illumination equations we learned in the lecture to implement components for 
    1. Diffuse
    2. Specular
    3. Ambient  
    You’ll implement the missing part in the Fragment shader source code. This part will be implemented in OpenGL Shading Language. Your code should iterate through all lights in the Light array.  

Ambient: SUM(I * ka)  (for all light)  
Diffuse: SUM(I * kd * (N.L))  (for all light, N.L > 0)  
Specular: SUM(I * ks * (N.L)^(kh))  (for all light, N.L > 0 and V.R > 0)

5. **Set up lights (TODO 4):** Set up lights:
    1. Use the Light struct which is defined above and the provided Light class to implement illumination equations for 3 different light sources.
        * Point light
        * Infinite light
        * Spotlight with radial and angular attenuation
    2. In the Sketch file Interrupt_keyboard method, bind keyboard interfaces that allow the user to toggle on/off specular, diffuse, and ambient with keys S, D, A.

Ambient: SUM(I * ka)  (for all light)  
Diffuse: SUM(I * kd * (N.L)) * f_radatt * f_angatt  (for all light, N.L > 0)  
Specular: SUM(I * ks * (V.R)^kh) * f_radatt * f_angatt  (for all light, N.L > 0 and V.R > 0)

Point Light: f_rad_att = 1, f_ang_att = 1  
Infinite light: f_rad_att = 1, f_ang_att = 1  
Spotlight: f_rad_att = 1 / (a + b * dis + c * dis^2), f_ang_att = angle^kf (inside) or 0 (outside)  

Toggle specular, diffuse, and ambient need extra flag in OpenGL -- "ambientOn", "diffuseOn", "specularOn".  
Check the flag before process light.

6. **Create your scenes (TODO 5):**
    1. We provide a fixed scene for you with preset lights, material, and model parameters. This scene will be used to examine your illumination implementation, and you should not modify it. 
    2. Create 3 new scenes (can be static scenes). Each of your scenes must have
        * at least 3 differently shaped solid objects
        * each object should have a different material
        * at least 2 lights
        * All types of lights should be used
    3. Provide a keyboard interface that allows the user to toggle on/off each of the lights in your scene model: Hit 1, 2, 3, 4, etc. to identify which light to toggle.

Scene one: Sphere and Torus. 3 point lights with animation.  
Scene two: Sphere. 1 spotlight, 1 point light.  
Scene Three: Sphere with texture and normal mapping, Torus and Cylinder. 1 spotlight, 2 point lights with animation.  
Scene Four: Sphere, Cylinder, Torus and Cube. 1 infinitely light, 1 point light.  
Scene Five: Normal rendering: Sphere, Cylinder, Torus and Cube. Texture and normal mapping: Sphere. Texture: Torus. 1 spotlight, 1 infinitely light, 2 point lights with animation.   

Switch scenes: store all scenes, scene index in Sketch.py initialization. Whenever key pressed, update index, and switch to new scene.  
Toggle light: Create extra flag variable in Light.py -- `lightOn`. Check this flag when process light in OpenGL. Created `SceneBase.py` to store this common function.

7. **Texture Mapping (BONUS FOR 480, 10 extra credits) (TODO 6/BONUS 6)**
    1. Set up each object's vertex texture coordinates(2D) to the self.vertices 9:11 columns (i.e. the last two columns). Tell OpenGL how to interpret these two columns: you need to set up attribPointer in the Displayable object's initialize method.
    2. Generate texture coordinates for the torus and sphere. Use “./assets/marble.jpg” for the torus and “./assets/earth.jpg” for the sphere as the texture image. There should be no seams in the resulting texture-mapped model. 

Calculate texture coordinate when generate Triangle Meshes. (range x: [0,1] y:[0,1])
Set texture color in OpenGL.  

### Extra Credit (10 points each, you may only receive up to 10 pts extra)

7. **Normal Mapping (BONUS 7)**
    1. Perform the same steps as Texture Mapping above, except that instead of using the image for vertex color, the image is used to modify the normals.
    2. Use the input normal map (“./assets/normalmap.jpg”) on both the sphere and the torus.

In order to read normal texture, we need to read extra texture data in OpenGL, called 'normalImage'. The step same as read texture.
Besides, local basis also needed. We have calculated in first step.
new normal = tColor.r * vPu + tColor.g * vPv + tColor.b * N;

### User Interface

The user interface to the program is provided through mouse buttons and keyboard keys.

**Left Mouse Dragging**: Rotate the camera\
**Middle Mouse Dragging**: Translate the camera\
**A**: Toggle Ambient Light\
**D**: Toggle Diffuse Light\
**S**: Toggle Specular Light\
**P**: Pause Animation\
**Left Arrow**: Go back to last scene\
**Right Arrow**: Next Scene\
**1,2,3, ...**: Toggle lights in current scene


