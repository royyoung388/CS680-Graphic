## Info
Name: Pengchao Yuan (U50962567)  
Assignment: CS680, PA3  
Reference: [Boids algorithm demonstration](https://eater.net/boids)

## Implementations

>1. **Predator/Prey Models:** To build your vivarium, you will first need to construct two different creatures using polyhedral (solid) parts. Implement your code as we did at "TODO 1" in the _ModelLinkage_ file.  
    * For the basic parts of your creatures, feel free to use routines provided with the previous assignment. You are also free to create your own basic parts, but they must be polyhedral (solid).  
    * The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae, fins, tentacles, etc.   
    * Model requirements:  
        1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body  
        2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at least one moving part.  
        3. The predator and prey should have distinguishable colors. You are welcome to reuse your PA2 creature in this assignment.   

Predator: reused pa2 model, it's a spider. Moving parts include 8 legs.  
Prey: new model - moth. Moving parts include 2 wings.

>2. **Model animation:** Use transforms to control the motion of each creature and its parts. Implement your code at "TODO 2," following the example of the _animationUpdate_ method in _ModelLinkage.py_.  
    * Set reasonable joint limits for your creature  
    * The creature's limbs should move back and forth in a periodic manner as it explores the vivarium. For example, a bird would continuously flap its wings.  

Predator: legs move in pairs.   
Prey: moth flap the wings.  

>3. **Collision Detection & Reaction:** Creatures in the vivarium should react to the positions of other creatures and move accordingly. Implement your code at "TODO 3" in the _stepForward_ method of the _ModelLinkage_ file.  
    * Your creature should always stay within the fixed-size 3D "tank". You should do collision detection between the creatures and tank walls. When creatures hit the tank walls, they should turn and change direction to stay within the tank.  
    * Your creatures should have a prey/predator relationship. For example, you could have a bug being chased by a spider, or a fish eluding a shark. This means your creature should react to the presence of other creatures in the tank.  
        * Use potential functions to change each creature's direction based on other creatures’ locations, their inter-creature distances, and their current configuration.  
        * You should detect collisions between creatures.   
            1. Predator-prey collision: The prey should disappear (get eaten) from the tank.  
            2. Collision between the same species: They should bounce apart from each other. You can use a reflection vector about a plane to decide the after-collision direction.  
        * You are welcome to use bounding spheres for collision detection.  
        * We recommend that you modularize shared functions (making two creatures bounce off each other, detecting if a creature is within the tank walls, etc.) within the _EnvironmentObject_ class. This will allow all creatures to inherit the same basic methods, which will form the backbone of each _stepForward_ routine.  
    * Your creatures should be able to move in 3 dimensions, not only on a plane.  

Keep in tank: for each aix, calculate the distance between creature and aix, if it's too close, add turn around velocity.  
Potential function: Gaussian potential function with different weight for different creatures.  
Collision: Sphere collision. Predator-prey collision: remove prey. Collision between the same species: 1. bounce off. 2. use boid algorithm

>4. **Creature orientation:** Creatures should face in the direction they are moving. For instance, a fish should be facing the direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions, so they should be able to face any direction in 3D space. Implement your code at "TODO 4" in the _rotateDirection_ method of _EnvironmentObject.py_.

Calculate rotation angle and pivot according to velocity direction.
`self.setQuaternion(self.rotateDirection(Point((0, 0, -1)), self.direction))`

>5. **(Extra credit for CS480 Students)** Feed your creatures with food: Add chunks of food to the vivarium which can be eaten by your creatures. See "BONUS 5(TODO 5)" in the _Vivarium_ file.   
    * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.   
    * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of the vivarium and remain there within the tank until eaten.  
    * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

Add keyboard interrupt in `Sketch.py`, and create food model. It keeps falling down. 

>6. **Flocking behavior:** Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors, for instance flocking together. This can be achieved by implementing the [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds. Implement your code at "BONUS 6" in the _ModelLinakge_ file.

Functions defined in `ModelPrey.py`  
`boid_cohesion`: find the center of boids, adjust direction slightly to the center  
`boid_separation`: Move away from other boids that are too close to avoid colliding   
`boid_alignment`: Find the average velocity (speed and direction) and match velocity  
Apply all functions on direction