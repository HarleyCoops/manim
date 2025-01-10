from manim import *
import numpy as np
from scipy.stats import norm

# Create a custom template for LaTeX
myTemplate = TexTemplate()
myTemplate.add_to_preamble(r"\usepackage{amsmath}")

class FinancialDerivativesScene(Scene):
    def construct(self):
        # Parameters for financial calculations
        S0 = 100  # Initial stock price
        K = 100   # Strike price
        r = 0.05  # Risk-free rate
        T = 1     # Time to maturity
        sigma = 0.2  # Volatility

        # 1. Discrete Random Walk
        def generate_random_walk(steps=100):
            return np.cumsum(np.random.normal(0, 1, steps))

        # Create coordinate system for random walk
        axes_walk = Axes(
            x_range=[0, 100, 20],
            y_range=[-10, 10, 5],
            axis_config={"include_tip": True},
        ).scale(0.7).to_edge(UP)

        title = Text("From Random Walk to Black-Scholes", font_size=24)
        title.to_edge(UP)
        self.play(Write(title))
        self.play(Create(axes_walk))

        # Generate and plot random walk
        walk_points = generate_random_walk()
        walk_points = [(i, point) for i, point in enumerate(walk_points)]
        random_walk = VMobject()
        random_walk.set_points_smoothly([axes_walk.c2p(x, y) for x, y in walk_points])
        random_walk.set_color(BLUE)
        
        self.play(Create(random_walk), run_time=2)
        self.wait()

        # 2. Transition to GBM
        # Create new axes for stock price
        axes_gbm = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 200, 50],
            axis_config={"include_tip": True},
        ).scale(0.7).next_to(axes_walk, DOWN, buff=0.5)

        gbm_label = Text("Geometric Brownian Motion", font_size=20)
        gbm_label.next_to(axes_gbm, UP)
        self.play(Create(axes_gbm), Write(gbm_label))

        # Generate GBM path
        def generate_gbm(S0, mu, sigma, T, steps):
            dt = T/steps
            t = np.linspace(0, T, steps)
            dW = np.random.normal(0, np.sqrt(dt), steps)
            W = np.cumsum(dW)
            return S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)

        gbm_points = generate_gbm(S0, r, sigma, T, 100)
        gbm_points = [(i, point) for i, point in enumerate(gbm_points)]
        gbm_path = VMobject()
        gbm_path.set_points_smoothly([axes_gbm.c2p(x, y) for x, y in gbm_points])
        gbm_path.set_color(GREEN)

        self.play(Create(gbm_path), run_time=2)
        self.wait()

        # 3. Black-Scholes Formula
        bs_title = Text("Black-Scholes Formula", font_size=30).next_to(axes_gbm, DOWN, buff=0.5)
        bs_formula = MathTex(
            "C = S_0N(d_1) - Ke^{-rT}N(d_2)", 
            tex_template=myTemplate,
            font_size=24
        ).next_to(bs_title, DOWN, buff=0.3)
        d1_d2 = MathTex(
            "d_1 = \\frac{\\ln(S_0/K) + (r + \\sigma^2/2)T}{\\sigma\\sqrt{T}},\\quad d_2 = d_1 - \\sigma\\sqrt{T}",
            tex_template=myTemplate,
            font_size=20
        ).next_to(bs_formula, DOWN, buff=0.3)

        self.play(Write(bs_title))
        self.play(Write(bs_formula))
        self.play(Write(d1_d2))
        self.wait()

        # 4. Option Payoff
        def call_payoff(S, K):
            return np.maximum(S - K, 0)

        # Generate final price distribution
        final_prices = np.linspace(50, 150, 100)
        payoffs = call_payoff(final_prices, K)
        
        axes_payoff = Axes(
            x_range=[50, 150, 25],
            y_range=[0, 50, 10],
            axis_config={"include_tip": True},
        ).scale(0.7).to_edge(RIGHT)

        payoff_points = [(price, payoff) for price, payoff in zip(final_prices, payoffs)]
        payoff_line = VMobject()
        payoff_line.set_points_smoothly([axes_payoff.c2p(x, y) for x, y in payoff_points])
        payoff_line.set_color(RED)

        payoff_label = Text("Option Payoff", font_size=20)
        payoff_label.next_to(axes_payoff, UP)

        self.play(Create(axes_payoff), Write(payoff_label))
        self.play(Create(payoff_line))
        self.wait()

        # 5. Final animation showing relationship
        arrows = VGroup()
        arrow1 = Arrow(random_walk.get_end(), gbm_path.get_start(), buff=0.1)
        arrow2 = Arrow(gbm_path.get_end(), payoff_line.get_start(), buff=0.1)
        arrows.add(arrow1, arrow2)
        
        self.play(Create(arrows))
        self.wait(2)

        # Fade out everything except the BS formula
        self.play(
            *[FadeOut(mob) for mob in [
                arrows, payoff_line, axes_payoff, payoff_label,
                gbm_path, axes_gbm, gbm_label,
                random_walk, axes_walk, title
            ]],
            bs_title.animate.move_to(ORIGIN).scale(1.5),
            bs_formula.animate.next_to(bs_title, DOWN, buff=0.3).scale(1.5),
            d1_d2.animate.next_to(bs_formula, DOWN, buff=0.3).scale(1.5)
        )
        self.wait(2)
