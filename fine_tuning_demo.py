from manim import *

class FineTuningDemo(Scene):
    def construct(self):
        # ----------------------------------------------------------
        # 1. INTRO TEXT
        # ----------------------------------------------------------
        title = Text("Fine-Tuning Demonstration").scale(0.9)
        subtitle = Text("How a Pre-trained Model Adapts to New Data").scale(0.6)
        subtitle.next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # ----------------------------------------------------------
        # 2. VISUALIZING A PRE-TRAINED MODEL
        # ----------------------------------------------------------
        # We'll represent a simple neural network with circles (neurons) and lines (connections).
        
        # Define circles for layers
        input_layer = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)]).arrange(DOWN, buff=0.5)
        hidden_layer = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(4)]).arrange(DOWN, buff=0.4)
        output_layer = VGroup(*[Circle(radius=0.3, color=RED) for _ in range(2)]).arrange(DOWN, buff=0.6)

        # Position the layers
        hidden_layer.next_to(input_layer, RIGHT, buff=2)
        output_layer.next_to(hidden_layer, RIGHT, buff=2)

        # Group them for easy manipulation
        network = VGroup(input_layer, hidden_layer, output_layer).move_to(ORIGIN)

        # Draw the network
        self.play(LaggedStartMap(FadeIn, input_layer, lag_ratio=0.2))
        self.play(LaggedStartMap(FadeIn, hidden_layer, lag_ratio=0.2))
        self.play(LaggedStartMap(FadeIn, output_layer, lag_ratio=0.2))

        # Connect the layers with lines (edges)
        connections = VGroup()
        for n1 in input_layer:
            for n2 in hidden_layer:
                line = Line(n1.get_right(), n2.get_left()).set_stroke(width=1)
                connections.add(line)
        for n1 in hidden_layer:
            for n2 in output_layer:
                line = Line(n1.get_right(), n2.get_left()).set_stroke(width=1)
                connections.add(line)

        self.play(Create(connections))
        self.wait(1)

        # Label this network as "Pre-trained Model"
        pre_trained_label = Text("Pre-trained Model").scale(0.5)
        pre_trained_label.next_to(network, UP)
        self.play(FadeIn(pre_trained_label))
        self.wait(1)

        # ----------------------------------------------------------
        # 3. SHOWING FINE-TUNING: NEW DATA & PARAMETER UPDATES
        # ----------------------------------------------------------
        # We'll conceptually show "new data" arriving and the model adjusting.

        # Add a representation for new data
        new_data_rect = Rectangle(height=2, width=3, color=YELLOW).move_to(3*DOWN + 4*LEFT)
        new_data_text = Text("New Data").scale(0.6).move_to(new_data_rect.get_center())
        new_data_group = VGroup(new_data_rect, new_data_text)
        self.play(FadeIn(new_data_group))

        # Animate "new data" moving into the network
        self.play(new_data_group.animate.shift(4.5 * RIGHT))

        # Emphasize update
        update_text = Text("Updating Parameters...").scale(0.5).set_color(YELLOW)
        update_text.next_to(network, DOWN, buff=1)
        self.play(Write(update_text))

        # Change color of connections to represent updated weights
        updated_connections = connections.copy().set_color(YELLOW)
        self.play(Transform(connections, updated_connections))

        # Label the network as "Fine-tuned Model"
        fine_tuned_label = Text("Fine-tuned Model").scale(0.5).set_color(YELLOW)
        fine_tuned_label.next_to(network, UP)
        self.play(ReplacementTransform(pre_trained_label, fine_tuned_label))

        self.wait(2)

        # ----------------------------------------------------------
        # 4. SUMMARIZE
        # ----------------------------------------------------------
        summary_box = Rectangle(height=2, width=6, color=WHITE).move_to(3*DOWN)
        summary_text = Text(
            "Fine-tuning takes a pre-trained model\n"
            "and adapts it to a new dataset,\n"
            "updating parameters along the way."
        ).scale(0.5).move_to(summary_box.get_center())

        summary_group = VGroup(summary_box, summary_text)
        self.play(FadeIn(summary_group))
        self.wait(3)

        # End
        self.play(FadeOut(network), FadeOut(connections), FadeOut(new_data_group), FadeOut(summary_group), FadeOut(update_text))
        self.wait(1)
