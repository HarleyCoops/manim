from manim import *
import numpy as np
import math

class QuantumFieldTheoryScene(ThreeDScene):
    def construct(self):
        # ----------------------------------------------------------
        # 1. STARFIELD BACKDROP
        # ----------------------------------------------------------
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.camera.background_color = "#000000"  # black background for a cosmic feel

        star_count = 300
        star_dots = VGroup(*[
            Dot3D(
                point=[np.random.uniform(-8, 8),
                       np.random.uniform(-5, 5),
                       np.random.uniform(-3, 3)],
                radius=np.random.uniform(0.002, 0.015),
                color=WHITE
            )
            for _ in range(star_count)
        ])

        self.play(FadeIn(star_dots, run_time=3))
        self.wait(1)

        # ----------------------------------------------------------
        # 2. MAIN TITLE
        # ----------------------------------------------------------
        main_title = Text(
            "Quantum Field Theory:\nA Journey into the Electromagnetic Interaction",
            font_size=42,
            gradient=(BLUE, TEAL)
        ).to_edge(UP)

        self.play(Write(main_title), run_time=3)
        self.wait(2)

        # Shrink and move title to upper-left corner
        self.play(
            main_title.animate.scale(0.5).to_corner(UL),
            run_time=2
        )
        self.wait(1)

        # ----------------------------------------------------------
        # 3. MINKOWSKI SPACETIME WIREFRAME + LIGHT CONE
        # ----------------------------------------------------------
        # We'll treat it as a 3D Axes for demonstration
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3],
            x_length=6,
            y_length=6,
            z_length=6,
            tips=False
        ).set_opacity(0.6)

        # Add labels (x,y,z) just for reference
        axis_labels = VGroup(
            Text("x").move_to(axes.c2p(3, 0, 0)),
            Text("y").move_to(axes.c2p(0, 3, 0)),
            Text("t").move_to(axes.c2p(0, 0, 3))
        ).scale(0.5).set_opacity(0.7)

        self.play(Create(axes), FadeIn(axis_labels), run_time=2)
        self.wait(1)

        # Light cone: we parametrize it
        def generate_light_cone():
            group = VGroup()
            num_rays = 24
            rmax = 2.5
            # We'll create multiple "lines" for the cone
            for k in range(num_rays):
                theta = 2*PI*k/num_rays
                line_upper = ParametricFunction(
                    lambda u: np.array([
                        u * np.cos(theta),
                        u * np.sin(theta),
                        u
                    ]),
                    t_range=[0, rmax],
                    color=YELLOW
                )
                line_lower = ParametricFunction(
                    lambda u: np.array([
                        u * np.cos(theta),
                        u * np.sin(theta),
                        -u  # negative t
                    ]),
                    t_range=[0, rmax],
                    color=YELLOW
                )
                group.add(line_upper, line_lower)
            return group

        light_cone = generate_light_cone().set_opacity(0.7)

        self.play(LaggedStartMap(Create, light_cone, lag_ratio=0.05), run_time=3)
        self.wait(1)

        # ----------------------------------------------------------
        # 4. COLOR-CODED METRIC EQUATION
        # ----------------------------------------------------------
        metric_equation = MathTex(
            r"{ds^2} = "
            r"-{c^2 dt^2}"
            r" + {dx^2}"
            r" + {dy^2}"
            r" + {dz^2}",
            font_size=36
        ).to_corner(UR)

        # Color the terms after creation
        metric_equation[0][0:3].set_color(RED)  # ds^2
        metric_equation[0][6:13].set_color(BLUE)  # c^2 dt^2
        metric_equation[0][14:18].set_color(GREEN)  # dx^2
        metric_equation[0][19:23].set_color(PURPLE)  # dy^2
        metric_equation[0][24:28].set_color(YELLOW)  # dz^2

        self.add_fixed_in_frame_mobjects(metric_equation)
        self.play(Write(metric_equation), run_time=3)
        self.wait(1)

        # Begin a slow rotation
        self.begin_ambient_camera_rotation(rate=0.1)

        # ----------------------------------------------------------
        # 5. ELECTRIC & MAGNETIC FIELD WAVES
        # ----------------------------------------------------------
        # We'll create a ghostly overlay near the origin
        wave_group = VGroup()
        wave_length = 3
        resolution = 50

        # Label arrows for E and B
        e_label = MathTex(r"\vec{E}", color=RED).scale(0.7)
        b_label = MathTex(r"\vec{B}", color=BLUE).scale(0.7)

        def get_em_wave(t):
            # E wave along y, B wave along z, wave propagates along x
            e_wave = ParametricFunction(
                lambda u: np.array([u, 0.6*math.sin(u - t), 0]),
                t_range=[-wave_length, wave_length],
                color=RED
            )
            b_wave = ParametricFunction(
                lambda u: np.array([u, 0, 0.6*math.sin(u - t)]),
                t_range=[-wave_length, wave_length],
                color=BLUE
            )
            return VGroup(e_wave, b_wave)

        # We'll animate the wave with an updater
        wave = get_em_wave(0)
        wave.add_updater(
            lambda mob, dt: mob.become(get_em_wave(self.time * 2))  # speed factor 2
        )

        # Place E and B labels near the "peak" of each wave
        e_label.move_to([wave_length*0.5, 0.6*math.sin(wave_length*0.5), 0]) 
        b_label.move_to([wave_length*0.5, 0, 0.6*math.sin(wave_length*0.5)])
        
        wave_group.add(wave, e_label, b_label)
        self.add(wave_group)
        self.wait(2)

        # ----------------------------------------------------------
        # 6. MAXWELL’S EQUATIONS TRANSFORMATION
        # ----------------------------------------------------------
        # Show Maxwell's eqn in one form, then morph into 4-vector form
        maxwell_eqn_1 = MathTex(
            r"\nabla \cdot \vec{E} = \frac{\rho}{\varepsilon_0}, \quad "
            r"\nabla \times \vec{E} = -\frac{\partial \vec{B}}{\partial t}, \quad "
            r"\dots",
            font_size=32
        ).to_edge(DR)

        self.add_fixed_in_frame_mobjects(maxwell_eqn_1)
        self.play(FadeIn(maxwell_eqn_1))
        self.wait(2)

        maxwell_eqn_2 = MathTex(
            r"\partial_\mu F^{\mu \nu} = \mu_0 J^\nu",
            font_size=34
        ).move_to(maxwell_eqn_1.get_center())

        # Morph the equation
        self.play(Transform(maxwell_eqn_1, maxwell_eqn_2), run_time=3)
        self.wait(2)

        # ----------------------------------------------------------
        # 7. QED LAGRANGIAN WITH COLOR CODING + PULSE
        # ----------------------------------------------------------
        # Now we project the QED Lagrangian onto a “semi-transparent plane”
        # We'll make a rectangle, put the eqn on it, and place them in 3D space
        plane_for_lagrangian = Rectangle(
            width=6, height=2.5, fill_opacity=0.3, fill_color=BLACK
        )
        plane_for_lagrangian.rotate_about_origin(PI/8, UP)  # slightly angled
        plane_for_lagrangian.shift(2*LEFT + 1*UP)

        # Color-coded QED Lagrangian
        # \psi in orange, D_\mu in green, gamma^\mu in teal, F_{\mu\nu} in gold
        qed_lagr = MathTex(
            r"\mathcal{L}_{\text{QED}} = \textcolor{orange}{\bar{\psi}} \bigl("
            r"i \textcolor{teal}{\gamma^\mu} \textcolor{green}{D_\mu} - m\bigr)\textcolor{orange}{\psi} "
            r"- \tfrac{1}{4}\textcolor{gold}{F_{\mu\nu}F^{\mu\nu}}",
            font_size=28
        )

        qed_lagr.move_to(plane_for_lagrangian.get_center())

        # A gentle pulsing effect on the eqn
        def pulse_lagration(mob, dt):
            scale_factor = 1 + 0.01*math.sin(2*PI*self.time)
            mob.scale_about_point(scale_factor, mob.get_center())

        # We'll add the plane and the eqn to a group so we can shift them at once
        lagr_group = VGroup(plane_for_lagrangian, qed_lagr)

        # Place the group in the 3D scene
        self.add(lagr_group)
        # Animate appearance
        self.play(FadeIn(plane_for_lagrangian), Write(qed_lagr), run_time=3)
        self.wait(1)

        # Optionally attach an updater (comment out if it causes weird effects)
        qed_lagr.add_updater(pulse_lagration)

        # ----------------------------------------------------------
        # 8. GAUGE INVARIANCE QUICK DEMO
        # ----------------------------------------------------------
        # Animate \psi gaining a phase factor e^{i alpha(x)}
        gauge_text = MathTex(r"\psi \to \psi' = e^{i\alpha(x)}\,\psi", font_size=28).next_to(lagr_group, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(gauge_text)
        self.play(FadeIn(gauge_text))
        self.wait(2)
        self.play(FadeOut(gauge_text))

        # ----------------------------------------------------------
        # 9. FEYNMAN DIAGRAM
        # ----------------------------------------------------------
        # Switch the camera or fade out the Minkowski axes, focusing on a black background
        fade_list = [axes, axis_labels, light_cone, maxwell_eqn_1, star_dots]  # keep wave, Lagr
        self.play(*[FadeOut(m) for m in fade_list], run_time=2)

        # Let’s put a big black rectangle behind everything
        black_bg = Rectangle(width=FRAME_WIDTH*2, height=FRAME_HEIGHT*2, fill_color=BLACK, fill_opacity=1)
        black_bg.move_to(ORIGIN)
        self.add(black_bg)
        self.bring_to_back(black_bg)

        # A simple Feynman diagram: 2 electron lines exchanging a photon
        e_left = Line(LEFT*4+DOWN*1.5, ORIGIN+DOWN*1.5).set_stroke(width=3).set_color(BLUE)
        e_right = Line(ORIGIN+DOWN*1.5, RIGHT*4+DOWN*1.5).set_stroke(width=3).set_color(BLUE)
        photon_line = CurvedArrow(
            start_point=(0, -1.5, 0),
            end_point=(0, 0.5, 0),
            angle=TAU/4,
            color=YELLOW
        ).set_stroke(width=3)

        e_left_label = MathTex(r"e^-", font_size=30, color=BLUE).next_to(e_left, DOWN)
        e_right_label = MathTex(r"e^-", font_size=30, color=BLUE).next_to(e_right, DOWN)
        photon_label = MathTex(r"\gamma", font_size=30, color=YELLOW).move_to(photon_line.get_center()+0.5*RIGHT)

        feynman_group = VGroup(e_left, e_right, photon_line, e_left_label, e_right_label, photon_label)
        feynman_group.shift(UP*0.5)

        self.play(Create(e_left), Create(e_right), Create(photon_line), FadeIn(e_left_label), FadeIn(e_right_label), FadeIn(photon_label), run_time=4)
        self.wait(1)

        # Animate coupling constant alpha ~ 1/137
        alpha_text = MathTex(r"\alpha \approx \frac{1}{137}", font_size=36, color=WHITE).next_to(feynman_group, UP, buff=0.3)
        self.play(FadeIn(alpha_text))
        self.wait(2)

        # Morph to symbolic alpha
        alpha_symbolic = MathTex(r"\alpha = \frac{e^2}{4 \pi \varepsilon_0 \hbar c}", font_size=36, color=WHITE)
        alpha_symbolic.move_to(alpha_text.get_center())
        self.play(Transform(alpha_text, alpha_symbolic), run_time=3)
        self.wait(2)

        # ----------------------------------------------------------
        # 10. RUNNING COUPLING GRAPH
        # ----------------------------------------------------------
        # We fade out the feynman diagram, show a 2D graph of alpha vs. energy
        self.play(*[FadeOut(m) for m in [feynman_group, alpha_text]], run_time=2)

        axes_2d = Axes(
            x_range=[0, 10, 2],
            y_range=[0.007, 0.015, 0.001],
            x_length=6, y_length=3,
            axis_config={"include_numbers": True},
            tips=True
        ).to_edge(DOWN).shift(LEFT*2)

        coupling_label_y = axes_2d.get_y_axis_label("Coupling Strength")
        scale_label_x = axes_2d.get_x_axis_label("Energy Scale")

        # A mock function for alpha running
        def alpha_run(x):
            # grows from ~1/137 ~0.0073 up to ~0.015 across x=0..10
            return 0.0073 + 0.0008*x**0.5

        alpha_graph = axes_2d.plot(alpha_run, [0, 10], color=YELLOW)
        alpha_points = VGroup()
        for i in range(6):
            x_val = i * 2
            y_val = alpha_run(x_val)
            dot = Dot(axes_2d.c2p(x_val, y_val, 0), color=RED)
            alpha_points.add(dot)

        graph_group = VGroup(axes_2d, scale_label_x, coupling_label_y, alpha_graph, alpha_points)
        self.play(Create(axes_2d), Write(scale_label_x), Write(coupling_label_y), run_time=2)
        self.play(Create(alpha_graph), LaggedStartMap(FadeIn, alpha_points, lag_ratio=0.2), run_time=3)
        self.wait(2)

        # Some short text clarifying vacuum polarization
        vacuum_text = Text("Vacuum polarization\nincreases α at higher energies", font_size=24, color=WHITE).next_to(axes_2d, UP)
        self.play(FadeIn(vacuum_text))
        self.wait(2)

        self.play(FadeOut(vacuum_text))

        # ----------------------------------------------------------
        # 11. OUTRO: ZOOM OUT TO COLLAGE & SUMMARY
        # ----------------------------------------------------------
        # Fade away 2D graph
        self.play(FadeOut(graph_group), run_time=2)

        # Bring back starfield & wave, Mink axes, Lagr, etc. as a “collage”
        # For clarity, let's just create a collage effect quickly
        self.play(FadeIn(star_dots), FadeIn(axes), FadeIn(axis_labels), FadeIn(light_cone))
        plane_for_lagrangian.set_opacity(0.4)
        self.play(FadeIn(plane_for_lagrangian), FadeIn(qed_lagr))
        self.play(FadeIn(wave_group))

        # Final text
        summary_text = Text(
            "QED: Unifying Light and Matter Through Gauge Theory",
            font_size=36,
            gradient=(YELLOW, GOLD)
        ).to_edge(DOWN)

        self.add_fixed_in_frame_mobjects(summary_text)
        self.play(FadeIn(summary_text))
        self.wait(3)

        # Camera slowly pulls away
        self.move_camera(phi=70*DEGREES, theta=-30*DEGREES, zoom=3.0, run_time=4)

        # Final subtitle "Finis"
        finis_text = Text("Finis", font_size=32, color=GREY_C).scale(1.2).to_edge(DOWN)
        self.play(Transform(summary_text, finis_text), run_time=2)
        self.wait(2)

        # Fade out everything
        self.stop_ambient_camera_rotation()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=3
        )
        self.wait(1)
