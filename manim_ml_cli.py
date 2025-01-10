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

    # Create the scene code
    scene_code = """from manim import *

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
"""

    # Write scene to temporary file
    with open('temp_scene.py', 'w') as f:
        f.write(scene_code)

    return scene_code

@click.command()
@click.argument('description', type=str)
@click.option('--quality', '-q', type=click.Choice(['l', 'm', 'h']), default='m', help='Animation quality (l/m/h)')
@click.option('--preview', '-p', is_flag=True, help='Preview animation after rendering')
def main(description, quality, preview):
    """Generate and render Manim animations from natural language descriptions.
    
    DESCRIPTION: A natural language description of the animation to visualize.
    """
    print(f"Generating animation for: {description}")
    
    # Generate the scene code
    scene_code = generate_scene_code(description)
    
    # Build manim command
    preview_flag = '-p' if preview else ''
    cmd = f'python -m manim {preview_flag} -q{quality} temp_scene.py GeneratedScene'
    
    # Run manim
    print("Rendering animation...")
    process = subprocess.run(cmd, shell=True, cwd=os.getcwd())
    
    if process.returncode == 0:
        output_path = Path('media/videos/temp_scene/480p15/GeneratedScene.mp4')
        if output_path.exists():
            print(f"\nAnimation saved to: {output_path}")
        else:
            print("\nAnimation generated but not found in expected location")
    else:
        print("\nError generating animation")

if __name__ == '__main__':
    main()
