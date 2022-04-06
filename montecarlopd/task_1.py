"""
=== Task 1: inverse and reject sampling ===
"""

from time import perf_counter

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from dataclasses import dataclass


@dataclass
class ClassedPoints:
    x_pass: np.array
    y_pass: np.array
    x_rej: np.array
    y_rej: np.array


def gen_numbers(mn: float, mx: float, n: float):
    # Generating n uniform random numbers between mn and mx
    return np.random.uniform(mn, mx, int(n))


def p_prime(x: np.array) -> np.array:
    # Function to form a dist. of
    return np.sin(x)


def q_inv(x: np.array) -> np.array:
    # Inverse of integral of p_prime(x), equation in report
    return np.arccos(1 - x)


def area(mn: float, mx: float, n: float, y: np.array) -> float:
    # Determines area by multiplying fraction of points by dimensions of graph
    return (mx - mn) * (1 - 0) * len(y) / n


def std(curve1: np.array, curve2: np.array, n: float) -> float:
    return np.sqrt(sum((curve1 - curve2) ** 2) / (n - 1))


class Task1:
    def __init__(self, inverse_samples: float, reject_samples: float):
        self.inverse_samples = inverse_samples
        self.reject_samples = reject_samples
        self.theta_array = np.linspace(0, np.pi)  # x axis

    def run(self):
        print('Task 1.1: Inverse sampling is now running')
        self.inverse_sampling()

        print('\nTask 1.2: Reject sampling is now running')
        self.rejection_sampling()

    def inverse_sampling(self):
        t1 = perf_counter()

        # Generate n many random nums between 0-2 (range of q_inv given range 0 < x < pi for p_prime)
        rand_num = gen_numbers(0, 2, self.inverse_samples)
        print(f"The time taken for {self.inverse_samples} samples was {perf_counter() - t1}s")

        sinified = q_inv(rand_num)
        error = self._histogram(sinified, 60, self.inverse_samples, "mediumseagreen", "Inverse Sampling")
        print(f"The error between the predicted and observed curves is: {error}")
        plt.show()

    def rejection_sampling(self):
        t1 = perf_counter()
        # Obtain rejected and accepted points
        points = self._gen_and_class_points(0, np.pi)
        area_under_curve = area(0, np.pi, self.reject_samples, points.y_pass)
        print(f"The time taken for {self.reject_samples} samples was {perf_counter() - t1}s")

        self._scatter(points, "cornflowerblue", "orange", "Rejection Sampling")
        plt.show()

        print("The area under the curve should be: 2")
        print(f"Area under the curve actually is: {area_under_curve}")
        print(f"The fraction of points under the curve is: {len(points.x_pass) / self.reject_samples}")

        error = self._histogram(points.x_pass, 60, len(points.x_pass), "cornflowerblue", "Rejection Sampling")
        print(f"The error between the predicted and observed curves is {error}")
        plt.show()

    def _gen_and_class_points(self, mn: float, mx: float) -> ClassedPoints:
        rand_x = gen_numbers(mn, mx, int(self.reject_samples))  # Random number between min and max values
        rand_y = gen_numbers(np.min(p_prime(self.theta_array)), np.max(p_prime(self.theta_array)), self.reject_samples)

        # If y value outside of sine curve for respective x (programmatically rand_x <= p_prime(rand_y))
        rejected = np.greater_equal(rand_y, p_prime(rand_x))
        passed = np.logical_not(rejected)

        return ClassedPoints(rand_x[passed], rand_y[passed], rand_x[rejected], rand_y[rejected])

    def _histogram(self, data: np.array, bin_num: int, n_samples: float, color: str, title: str) -> float:
        bin_width = np.pi / bin_num  # For normalising sine plot
        norm = n_samples / 2 * bin_width

        plt.hist(data, bins=bin_num, color=color, alpha=0.7)
        plt.xlabel(r'$\theta$ 'r'$(0 < \theta < \pi)$')
        plt.ylabel('Frequency')
        plt.title(f'-- {title} --\nHistogram of generated 'r'$\theta$ (n=1x10'r'$^{4}$)')

        g_kde = gaussian_kde(data)  # Gaussian KDE of the data
        plt.plot(self.theta_array, norm * p_prime(self.theta_array), c='r',  # Plotting sine
                 label='sin('r'$\theta$)')
        plt.plot(self.theta_array, 2 * norm * g_kde.evaluate(self.theta_array), c="black",
                 linestyle="--", label="Gaussian KDE")  # Plotting Gaussian KDE
        plt.legend()

        # Error between gkde and p_prime(x)
        return std(g_kde.evaluate(self.theta_array), p_prime(self.theta_array), n_samples)

    def _scatter(self, points: ClassedPoints, color_pass: str, color_rej: str, title: str):
        # Plots a scatter plot and overlays scaled sine curve over top
        plt.title(f'-- {title} --\nScatter plot of accepted random points (n=1x10'r'$^{4}$)')
        plt.xlabel(r'$\theta$ 'r'$(0 < \theta < \pi)$')
        plt.ylabel('y')
        plt.scatter(points.x_pass, points.y_pass, s=1, c=color_pass)  # Scatter accepted points under curve
        plt.scatter(points.x_rej, points.y_rej, s=1, c=color_rej)
        plt.plot(self.theta_array, p_prime(self.theta_array), color='r')  # Overlaid sine curve
