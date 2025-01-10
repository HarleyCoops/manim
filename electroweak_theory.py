from manim import *
import math
import numpy as np

class ElectroweakTheoryScene(ThreeDScene):
    """
    A sophisticated Manim 3D scene illustrating the fundamental concepts of
    electroweak theory and symmetry breaking, including gauge fields,
    particle interactions, and the Higgs mechanism.
    """
    def construct(self):
        # ----------------------------------------------------------
        # 1. INITIAL SETUP AND INTRO
        # ----------------------------------------------------------
        # Configure the initial 3D camera orientation and background
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.camera.background_color = "#000000"  # Pure black background

        # Main title with gradient effect
        title = Text(
            "Gauge Fields and the Nature of\nElectroweak Symmetry Breaking",
            font_size=48,
            gradient=(BLUE, GREEN)
        ).to_edge(UP)
        
        subtitle = Text(
            "A Journey Through Symmetry and Mass",
            font_size=36,
            color=BLUE_A
        ).next_to(title, DOWN, buff=0.3)

        # Fade in titles
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)

        # Move to corner
        self.play(
            title.animate.scale(0.4).to_corner(UR),
            subtitle.animate.scale(0.4).next_to(title, DOWN, buff=0.1),
            run_time=2
        )

        # ----------------------------------------------------------
        # 2. THEORETICAL FRAMEWORK - LAGRANGIAN
        # ----------------------------------------------------------
        # Create the electroweak Lagrangian in parts
        lagrangian_parts = [
            MathTex(
                r"\mathcal{L}_{\text{EW}} = -\tfrac{1}{4} W_{\mu\nu}^a W^{a\,\mu\nu}",
                font_size=36
            ),
            MathTex(
                r"-\tfrac{1}{4} B_{\mu\nu} B^{\mu\nu}",
                font_size=36
            ),
            MathTex(
                r"+ \bar{\psi}_L \gamma^\mu \left(i \partial_\mu - g \tfrac{\sigma^a}{2} W_\mu^a - g' Y B_\mu \right)\psi_L",
                font_size=36
            )
        ]

        # Position them in a column
        VGroup(*lagrangian_parts).arrange(DOWN, buff=0.3).shift(2*LEFT + UP)
        
        # Add as fixed frame mobjects so they don't rotate with 3D scene
        for part in lagrangian_parts:
            self.add_fixed_in_frame_mobjects(part)
            self.play(Write(part), run_time=2)
            self.wait(0.5)

        # ----------------------------------------------------------
        # 3. PARTICLE REPRESENTATION AND FIELDS
        # ----------------------------------------------------------
        def create_particle(name, color, position, radius=0.2):
            sphere = Sphere(radius=radius, color=color)
            label = MathTex(name, color=color)
            label.next_to(sphere, DOWN)
            return VGroup(sphere, label).move_to(position)

        # Create fundamental particles
        particles = VGroup(
            create_particle("e^-", BLUE, LEFT * 2),
            create_particle("\\nu_e", BLUE_E, LEFT),
            create_particle("W^+", YELLOW, RIGHT),
            create_particle("Z^0", GOLD, RIGHT * 2),
            create_particle("\\gamma", WHITE, UP * 2)
        )

        # Create a 3D grid
        grid = NumberPlane(
            x_range=(-8, 8, 1),
            y_range=(-8, 8, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        grid.rotate(PI/2, RIGHT)
        
        # Add particles and grid
        self.play(Create(grid), run_time=2)
        self.play(*[Create(p) for p in particles], run_time=3)

        # ----------------------------------------------------------
        # 4. HIGGS MECHANISM VISUALIZATION
        # ----------------------------------------------------------
        def mexican_hat(u, v):
            r = np.sqrt(u**2 + v**2)
            return 0.25 * (r**2 - 1)**2

        # Create Mexican hat potential surface
        potential = Surface(
            lambda u, v: np.array([u, v, mexican_hat(u, v)]),
            u_range=(-2, 2),
            v_range=(-2, 2),
            resolution=(32, 32),
            fill_opacity=0.8,
            checkerboard_colors=[GOLD_D, GOLD_E]
        )
        potential.shift(DOWN * 2)

        # Add potential surface
        self.play(Create(potential), run_time=3)

        # Create sphere for symmetry breaking visualization
        breaking_sphere = Sphere(radius=0.1, color=RED)
        breaking_sphere.move_to(potential.get_top())

        def sphere_path(t):
            radius = 1
            angle = t * 2 * PI
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = mexican_hat(x, y)
            return np.array([x, y, z - 1.8])  # Adjust z to match potential surface

        # Animate symmetry breaking
        self.play(Create(breaking_sphere))
        self.play(
            MoveAlongPath(
                breaking_sphere,
                ParametricFunction(sphere_path, t_range=[0, 1]),
            ),
            run_time=4
        )

        # ----------------------------------------------------------
        # 5. DYNAMIC FIELD VISUALIZATION
        # ----------------------------------------------------------
        # Create a transparent sphere representing the Higgs field
        higgs_field = Sphere(radius=0.1, color=PURPLE).set_opacity(0.3)
        higgs_field.shift(DOWN * 2)

        def update_higgs_field(mob, alpha):
            new_radius = 4 * alpha + 0.1
            mob.become(
                Sphere(radius=new_radius, color=PURPLE)
                .set_opacity(0.2 * (1 - alpha))
                .shift(DOWN * 2)
            )

        # Animate Higgs field expansion
        self.play(
            UpdateFromAlphaFunc(higgs_field, update_higgs_field),
            run_time=3,
            rate_func=there_and_back
        )

        # ----------------------------------------------------------
        # 6. CAMERA MOVEMENT AND FINAL DISPLAY
        # ----------------------------------------------------------
        # Begin rotating camera
        self.begin_ambient_camera_rotation(rate=0.2)
        
        # Add final explanation
        explanation = Text(
            "Electroweak Symmetry Breaking:\nWhere Mass Emerges from Symmetry",
            font_size=36,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)

        # Stop camera rotation
        self.stop_ambient_camera_rotation()

        # Final fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
