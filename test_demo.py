from manim import *

class TestDemo(Scene):
    def construct(self):
        # Create a simple text object
        text = Text("Manim Test", color=BLUE)
        
        # Add animation
        self.play(Write(text))
        
        # Wait for a moment
        self.wait()
        
        # Move text
        self.play(text.animate.shift(UP * 2))
        
        # Final pause
        self.wait()
