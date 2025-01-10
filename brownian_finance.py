from manim import *
import numpy as np
from scipy.stats import norm

class BrownianFinanceScene(Scene):
    def construct(self):
        # Title
        title = Text("From Brownian Motion to Financial Markets", font_size=40)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        # Create Brownian motion simulation
        num_points = 200
        time = np.linspace(0, 4, num_points)
        np.random.seed(42)  # For reproducibility
        brownian_increments = np.random.normal(0, 0.1, num_points-1)
        brownian_path = np.cumsum(brownian_increments)
        brownian_path = np.insert(brownian_path, 0, 0)  # Start at 0

        # Create axes for Brownian motion
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-1, 1, 0.5],
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [-1, -0.5, 0, 0.5, 1]}
        ).scale(0.7)

        # Create the graph
        graph = axes.plot_line_graph(
            x_values=time,
            y_values=brownian_path,
            line_color=BLUE,
            vertex_dot_radius=0.0
        )

        # Labels
        x_label = axes.get_x_axis_label("Time")
        y_label = axes.get_y_axis_label("Price")
        graph_group = VGroup(axes, graph, x_label, y_label).to_edge(LEFT)

        # Add explanation
        explanation = Text(
            "Brownian Motion",
            font_size=24
        ).next_to(graph_group, UP)

        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(explanation)
        )
        self.play(Create(graph), run_time=2)
        self.wait()

        # Create GBM simulation
        drift = 0.2
        volatility = 0.3
        S0 = 1.0
        gbm_path = S0 * np.exp((drift - 0.5 * volatility**2) * time + 
                              volatility * brownian_path)

        # Create axes for GBM
        gbm_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 2, 0.5],
            axis_config={"include_tip": False},
            x_axis_config={"numbers_to_include": [0, 1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1, 1.5, 2]}
        ).scale(0.7)

        # Create the GBM graph
        gbm_graph = gbm_axes.plot_line_graph(
            x_values=time,
            y_values=gbm_path,
            line_color=GREEN,
            vertex_dot_radius=0.0
        )

        # Labels for GBM
        gbm_x_label = gbm_axes.get_x_axis_label("Time")
        gbm_y_label = gbm_axes.get_y_axis_label("Stock Price")
        gbm_group = VGroup(gbm_axes, gbm_graph, gbm_x_label, gbm_y_label).to_edge(RIGHT)

        gbm_explanation = Text(
            "Geometric Brownian Motion",
            font_size=24
        ).next_to(gbm_group, UP)

        self.play(
            Create(gbm_axes),
            Write(gbm_x_label),
            Write(gbm_y_label),
            Write(gbm_explanation)
        )
        self.play(Create(gbm_graph), run_time=2)
        self.wait()

        # Add Black-Scholes formula
        bs_formula = MathTex(
            "C = S_0N(d_1) - Ke^{-rT}N(d_2)",
            font_size=30
        ).next_to(title, DOWN)

        self.play(Write(bs_formula))
        self.wait(2)
