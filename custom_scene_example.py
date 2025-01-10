from manim import *

class CustomScene(Scene):
    def __init__(self, **kwargs):
        # You can pass custom parameters when creating the scene
        self.point_color = kwargs.get('point_color', BLUE)
        self.show_formula = kwargs.get('show_formula', True)
        super().__init__()

    def construct(self):
        # 1. Create and display title
        title = Text("Custom Animation", font_size=40)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # 2. Create main objects
        # You can customize these based on parameters
        circle = Circle(radius=2, color=self.point_color)
        dot = Dot(color=RED)
        
        # 3. Add animations
        self.play(Create(circle))
        self.play(dot.animate.move_to(circle.point_at_angle(0)))
        
        # 4. Conditional animations based on parameters
        if self.show_formula:
            formula = MathTex(r"e^{i\pi} + 1 = 0")
            formula.next_to(circle, DOWN)
            self.play(Write(formula))

        # 5. Wait at the end
        self.wait(2)

if __name__ == "__main__":
    # Example of how to run with different parameters
    scene = CustomScene(
        point_color=BLUE,
        show_formula=True
    )
    scene.render()
