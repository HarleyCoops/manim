import re
from manim import Scene

class MLAnimationGenerator:
    def __init__(self):
        self.templates = {
            'network': self._create_network_template,
            'training': self._create_training_template,
            'comparison': self._create_comparison_template
        }
        
    def _create_network_template(self, params):
        """Creates a neural network visualization with customizable layers"""
        class NetworkScene(Scene):
            def construct(self):
                # Parse parameters
                layer_sizes = params.get('layer_sizes', [3, 4, 3])
                title_text = params.get('title', 'Neural Network')
                
                # Create title
                title = Text(title_text).scale(0.8)
                title.to_edge(UP)
                
                # Create layers
                layers = []
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
                    LaggedStartMap(FadeIn, network, lag_ratio=0.2),
                    run_time=2
                )
                self.play(Create(connections, lag_ratio=0.1))
                self.wait()
                
        return NetworkScene

    def _create_training_template(self, params):
        """Creates a training progress visualization"""
        class TrainingScene(Scene):
            def construct(self):
                # Create progress elements
                epochs = params.get('epochs', 5)
                title = Text(params.get('title', 'Training Progress')).scale(0.8)
                title.to_edge(UP)
                
                # Create progress bar
                bar = Rectangle(height=0.4, width=6, color=BLUE)
                bar.move_to(ORIGIN)
                bar.set_fill(BLUE, opacity=0.1)
                
                # Create accuracy text
                accuracy = DecimalNumber(
                    0,
                    num_decimal_places=1,
                    include_sign=False,
                )
                accuracy_text = Text("Accuracy: ").scale(0.8)
                accuracy_label = VGroup(accuracy_text, accuracy)
                accuracy_label.arrange(RIGHT)
                accuracy_label.next_to(bar, UP)
                
                # Animations
                self.play(Write(title))
                self.play(Create(bar), Write(accuracy_label))
                
                # Training progress
                for i in range(epochs):
                    self.play(
                        bar.animate.set_fill(opacity=(i+1)/epochs),
                        accuracy.animate.set_value((i+1)*100/epochs),
                        run_time=0.5
                    )
                
                self.wait()
                
        return TrainingScene

    def _create_comparison_template(self, params):
        """Creates a side-by-side comparison visualization"""
        class ComparisonScene(Scene):
            def construct(self):
                # Create titles
                title1 = Text(params.get('title1', 'Model A')).scale(0.6)
                title2 = Text(params.get('title2', 'Model B')).scale(0.6)
                
                # Create comparison elements (e.g., accuracy bars)
                bar1 = Rectangle(height=params.get('value1', 0.6)*3, width=1, color=BLUE)
                bar2 = Rectangle(height=params.get('value2', 0.8)*3, width=1, color=RED)
                
                # Position elements
                title1.move_to(UP*2 + LEFT*2)
                title2.move_to(UP*2 + RIGHT*2)
                bar1.next_to(title1, DOWN)
                bar2.next_to(title2, DOWN)
                
                # Animations
                self.play(Write(title1), Write(title2))
                self.play(GrowFromEdge(bar1, DOWN), GrowFromEdge(bar2, DOWN))
                self.wait()
                
        return ComparisonScene

    def parse_description(self, text):
        """Parse natural language description into parameters for templates"""
        params = {}
        
        # Extract network architecture
        if 'layer' in text.lower():
            layer_match = re.findall(r'(\d+)\s*layer', text.lower())
            if layer_match:
                params['layer_sizes'] = [3] * (int(layer_match[0]))
        
        # Extract training parameters
        if 'epoch' in text.lower():
            epoch_match = re.findall(r'(\d+)\s*epoch', text.lower())
            if epoch_match:
                params['epochs'] = int(epoch_match[0])
        
        # Extract comparison values
        if 'compare' in text.lower() or 'versus' in text.lower():
            params['template'] = 'comparison'
            # Extract percentages or decimal values
            values = re.findall(r'(\d+(?:\.\d+)?)\s*%?', text)
            if len(values) >= 2:
                params['value1'] = float(values[0]) / 100
                params['value2'] = float(values[1]) / 100
        
        # Default to network template if no specific template is detected
        if 'template' not in params:
            if 'train' in text.lower() or 'progress' in text.lower():
                params['template'] = 'training'
            else:
                params['template'] = 'network'
        
        return params

    def generate_scene(self, description):
        """Generate a manim scene based on the description"""
        params = self.parse_description(description)
        template_name = params.pop('template', 'network')
        ParentSceneClass = self.templates[template_name](params)
        class GeneratedScene(ParentSceneClass):
            def construct(self):
                super().construct()
        return GeneratedScene

def create_animation(description):
    """Creates a Manim scene class based on the input description."""
    scene_code = """class GeneratedScene(Scene):
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
        self.wait()"""
        
    # Create a new class from the code
    namespace = {}
    exec(scene_code, globals(), namespace)
    return namespace['GeneratedScene']

# Example usage:
if __name__ == "__main__":
    # Example descriptions:
    descriptions = [
        "Show me a neural network with 4 layers",
        "Visualize training progress over 10 epochs",
        "Compare model A (75% accuracy) versus model B (85% accuracy)"
    ]
    
    # Generate scene for the first description
    Scene = create_animation(descriptions[0])
