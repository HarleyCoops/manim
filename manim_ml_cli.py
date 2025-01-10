#!/usr/bin/env python
import click
import re
import subprocess
import os
from pathlib import Path

def parse_network_structure(description):
    """Extract network structure from description."""
    # Look for layer specifications like "3 layers with 4,6,4 neurons" or "4-6-4 network"
    layer_spec = re.search(r'(\d+(?:[,-]\d+)*)', description)
    if layer_spec:
        # Convert to list of integers, handling both comma and hyphen separators
        layers = [int(x) for x in re.split(r'[,-]', layer_spec.group(1))]
        return layers
    
    # Default structure if none specified
    return [4, 6, 4]

def generate_scene_code(description):
    """Generate Manim scene code based on description."""
    layer_sizes = parse_network_structure(description)
    
    # Customize title based on description
    title = "Neural Network"
    if "classifier" in description.lower():
        title = "Neural Network Classifier"
    elif "autoencoder" in description.lower():
        title = "Autoencoder Network"
    
    # Choose colors based on description
    node_color = "BLUE"
    if "red" in description.lower():
        node_color = "RED"
    elif "green" in description.lower():
        node_color = "GREEN"

    scene_code = f'''from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create title
        title = Text("{title}", color={node_color}).scale(0.8)
        title.to_edge(UP)
        
        # Create layers
        layers = []
        layer_sizes = {layer_sizes}  # Network architecture
        
        for size in layer_sizes:
            layer = VGroup(*[Circle(radius=0.2, color={node_color}) for _ in range(size)])
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
        
        # Add layer labels
        labels = []
        layer_names = ["Input Layer", "Hidden Layer", "Output Layer"]
        if len(layers) == 2:
            layer_names = ["Input Layer", "Output Layer"]
        elif len(layers) > 3:
            layer_names = ["Input Layer"] + ["Hidden Layer {}".format(i) for i in range(1, len(layers)-1)] + ["Output Layer"]
        
        for layer, name in zip(layers, layer_names):
            label = Text(name, color=WHITE).scale(0.4)
            label.next_to(layer, DOWN, buff=0.5)
            labels.append(label)
        
        # Animations
        self.play(Write(title))
        
        # Create layers with labels
        for layer, label in zip(layers, labels):
            self.play(
                Create(layer),
                Write(label),
                run_time=1
            )
        
        # Create connections with a nice effect
        self.play(
            Create(connections, lag_ratio=0.1),
            run_time=2
        )
        
        if "pulse" in description.lower():
            # Add pulsing animation
            self.play(
                *[layer.animate.scale(1.2) for layer in layers],
                run_time=0.5
            )
            self.play(
                *[layer.animate.scale(1/1.2) for layer in layers],
                run_time=0.5
            )
        
        self.wait()

class TempScene(GeneratedScene):
    pass
'''
    return scene_code

@click.command()
@click.argument('description', required=True)
@click.option('--quality', '-q', default='l', 
              type=click.Choice(['l', 'm', 'h', 'k']),
              help='Animation quality (l=low, m=medium, h=high, k=4k)')
@click.option('--preview/--no-preview', '-p', default=True,
              help='Preview the animation after rendering')
def main(description, quality, preview):
    """Generate and render Manim animations from natural language descriptions.
    
    DESCRIPTION: A natural language description of the neural network to visualize.
    Examples:
    - "Show me a neural network with 3 layers"
    - "Create a red neural network with 4-8-4 neurons"
    - "Generate a classifier network with 5 layers and pulsing animation"
    """
    print(f"Generating animation for: {description}")
    
    # Generate the scene code
    scene_code = generate_scene_code(description)
    
    # Write to temporary file
    with open("temp_scene.py", "w") as f:
        f.write(scene_code)
    
    # Build manim command
    preview_flag = '-p' if preview else ''
    cmd = f'python -m manim {preview_flag}q{quality} temp_scene.py TempScene'
    
    # Run manim
    print("Rendering animation...")
    process = subprocess.run(cmd, shell=True, cwd=os.getcwd())
    
    if process.returncode == 0:
        output_path = Path('media/videos/temp_scene/480p15/TempScene.mp4')
        if output_path.exists():
            print(f"\nAnimation saved to: {output_path}")
        else:
            print("\nAnimation generated but not found in expected location")
    else:
        print("\nError generating animation")

if __name__ == '__main__':
    main()
