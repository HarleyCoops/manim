from manim import *

class SimpleModelTraining(Scene):
    def construct(self):
        # Create a title
        title = Text("Model Training Process", font_size=40)
        title.to_edge(UP)
        
        # Create initial accuracy text
        accuracy = DecimalNumber(
            0,
            show_ellipsis=True,
            num_decimal_places=2,
            include_sign=False,
        )
        accuracy_text = Text("Accuracy: ", font_size=36)
        accuracy_label = VGroup(accuracy_text, accuracy)
        accuracy_label.arrange(RIGHT)
        accuracy_label.next_to(title, DOWN, buff=1)
        
        # Create progress bar
        progress_bar = Rectangle(height=0.4, width=6, color=BLUE)
        progress_bar.next_to(accuracy_label, DOWN, buff=1)
        progress_bar.set_fill(BLUE, opacity=0.3)
        
        # Add elements to scene
        self.play(Write(title))
        self.play(Write(accuracy_label))
        self.play(Create(progress_bar))
        
        # Animate training progress
        for i in range(10):
            new_accuracy = i * 10
            self.play(
                accuracy.animate.set_value(new_accuracy),
                progress_bar.animate.set_fill(opacity=i/10),
                run_time=0.5
            )
        
        # Final state
        self.play(
            accuracy.animate.set_value(99.5),
            progress_bar.animate.set_fill(opacity=1),
            run_time=1
        )
        
        self.wait(2)
