from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create title
        title = Text("Trigonometric Functions").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create unit circle
        circle = Circle(radius=1, color=BLUE)
        self.play(Create(circle))
        self.wait()
