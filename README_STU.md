Pengchao Yuan (U50962567)  
CS 680, PA1

# common function
###*def bresenham(self, x1, y1, x2, y2)*
Bresenham algorithm generator.  
Input two point coordinates, return a Bresenham generator.

###*def point_generator(self, p1: Point, p2: Point, flat_Color: ColorType = None)*  
Bresenham point generator. Wrapper of bresenham algorithm. Combined with color interpolation.  
Input two points and color, return a point generator.

###*def aa_generator(self, x1, y1, x2, y2, doAAlevel)*  
Anti-aliasing generator. Wrapper of bresenham algorithm. Scale x, y according to aa level.  
Input two point coordinates and aa level, return a Bresenham generator

###*def texture_bilinear(self, x, y)*
Texture bi-linear interpolation.
Input coordinates, return ColorType.

# line rendering function
###*def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4)*
Use point_generator() and aa_generator() to generate points  

# triangle rendering function
###*def drawTriangle(self, buff, p1, p2, p3, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False)*  
Use point_generator() and aa_generator() to generate points.  
Draw the border first, then draw sacn line.   

# texture mapping
Use texture_bilinear() to calculate the texture color

# anti-aliased
Use aa_generator to calculate percentage of color.
