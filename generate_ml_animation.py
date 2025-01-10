from text_to_manim_converter import create_animation
import sys

def main():
    if len(sys.argv) > 1:
        description = " ".join(sys.argv[1:])
    else:
        description = "Show me a neural network with 4 layers"
    
    print(f"Generating animation for: {description}")
    
    # Create the scene class
    scene_code = """from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create title
        title = Text("Neural Network", color=BLUE).scale(0.8)
        title.to_edge(UP)
        
        # Create layers
        layers = []
        layer_sizes = [4, 6, 4]  # Input, hidden, output layers
        
        for size in layer_sizes:
            layer = VGroup(*[Circle(radius=0.2, color=BLUE) for _ in range(size)])
            layer.arrange(DOWN, buff=0.3)
            layers.append(layer)
        
        # Position layers
        network = VGroup(*layers).arrange(RIGHT, buff=2)
        network.move_to(ORIGIN)
        
        # Create connections
        connections = VGroup()
        for i in range(len(layers)-1):
            curr_layer = layers[i]
            next_layer = layers[i+1]
            for n1 in curr_layer:
                for n2 in next_layer:
                    line = Line(n1.get_right(), n2.get_left(), stroke_width=1)
                    connections.add(line)
        
        # Animations
        self.play(Write(title))
        self.play(
            *[Create(layer) for layer in layers],
            run_time=2
        )
        self.play(Create(connections, lag_ratio=0.1))
        self.wait()

class TempScene(GeneratedScene):
    pass
"""
    
    # Write the scene class to a temporary file
    with open("temp_scene.py", "w") as f:
        f.write(scene_code)

    print("Scene class written to temp_scene.py")

if __name__ == "__main__":
    main()
