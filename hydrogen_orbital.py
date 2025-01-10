from manim import *
import math
import numpy as np

class HydrogenOrbitalScene(ThreeDScene):
    def construct(self):
        # Set up camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # Create title with regular Text
        title = Text("Hydrogen 1s Orbital", color=BLUE).scale(0.8)
        subtitle = Text("Quantum Mechanical Visualization", color=BLUE_B).scale(0.4)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Create and show title
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Create axes for the radial plot
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Add axis labels
        x_label = Text("x").next_to(axes.x_axis, RIGHT)
        y_label = Text("y").next_to(axes.y_axis, UP)
        z_label = Text("z").next_to(axes.z_axis, OUT)
        labels = VGroup(x_label, y_label, z_label)
        
        self.play(Create(axes), Create(labels))
        
        # Create the orbital surface
        def get_orbital_surface(u, v):
            # Spherical coordinates to Cartesian
            r = 2  # Base radius
            x = r * np.sin(u) * np.cos(v)
            y = r * np.sin(u) * np.sin(v)
            z = r * np.cos(u)
            return np.array([x, y, z])
        
        orbital = Surface(
            func=get_orbital_surface,
            u_range=[0, PI],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=0.5,
            fill_color=BLUE,
            stroke_color=BLUE_A,
            stroke_width=0.5,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # Add the orbital with a nice animation
        self.play(Create(orbital))
        self.wait(1)
        
        # Add a pulsing animation to show wave nature
        self.play(
            orbital.animate.scale(1.2),
            rate_func=there_and_back,
            run_time=2
        )
        
        # Rotate the camera for better view
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # Add probability density explanation
        explanation = Text(
            "The surface represents regions\n"
            "where the electron is most\n"
            "likely to be found",
            color=WHITE,
            font_size=24
        ).to_corner(UR)
        
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)
        
        # Final rotation to show the complete orbital
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(orbital),
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(explanation)
        )
        self.wait(1)
