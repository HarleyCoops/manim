from manim import *

class SimpleScene(Scene):
    def construct(self):
        # Create a circle
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)

        # Create a square
        square = Square()
        square.set_fill(RED, opacity=0.5)

        # Add circle to scene
        self.play(Create(circle))
        
        # Transform circle to square
        self.play(Transform(circle, square))
        
        # Wait at end of animation
        self.wait()
