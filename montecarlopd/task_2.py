from typing import List, Tuple

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class OnTarget:
    x: np.array
    y: np.array
    x_smear: np.array
    y_smear: np.array


remove_elements_less_than = lambda arr, val: arr[arr > val]


def get_on_target(x: np.array, y: np.array, limit: float) -> np.array:
    # returns array of x and y less than limit
    matching_elements = np.logical_and(np.abs(x) < limit, np.abs(y) < limit)
    return x[matching_elements], y[matching_elements]


class Task2:
    def __init__(self, particle_samples: float):
        self.x_res = 0.1  # Resolution of the detector
        self.y_res = 0.3
        self.detector_size = 4  # length in m, square detector
        self.detector_emitter_distance = 2  # m

        self.particle_velocity = 2000  # m/s
        self.particle_samples = int(particle_samples)

    def run(self):
        print('Task 2: Modelling particle decays')
        self.particle_decay_mcm()

    def particle_decay_mcm(self):
        phi, theta = self._gen_angles()
        decay_distances = self._decay_distances()
        on_target = self._gen_xy(decay_distances, theta, phi)

        hist = self._hist_2d(on_target.x, on_target.y)
        print('Here is a 2d histogram and a jointplot for the unsmeared detector')
        self._jointplot(on_target.x, on_target.y)
        plt.show()

        hist_smear = self._hist_2d(on_target.x_smear, on_target.y_smear)
        self._jointplot(on_target.x_smear, on_target.y_smear)
        print('Here is a 2d histogram and a jointplot for the smeared detector')
        plt.show()

    def _gen_angles(self) -> Tuple:
        phi = np.arccos(1 - np.random.uniform(0, 1, self.particle_samples))  # Polar [0, pi/2]
        theta = np.random.uniform(0, 2 * np.pi, self.particle_samples)  # Azimuth [0, 2pi]
        return phi, theta

    # Creates array of decay distances using poission dist.
    def _decay_distances(self) -> np.array:
        times = np.random.exponential(550e-6, self.particle_samples)  # Decay times, mean is 550 microseconds
        return self.particle_velocity * times

    # Smears result with gaussian with standard deviation of resolution
    def _smear(self, x: np.array, y: np.array) -> Tuple:
        x = np.random.normal(x, self.x_res)
        y = np.random.normal(y, self.y_res)
        return x, y

    def _gen_xy(self, decay_distances: np.array, theta_arr: np.array, phi_arr: np.array) -> OnTarget:
        # Converts spherical co-ords into cartesian on x-y plane
        detector_half_size = self.detector_size / 2

        pre_target = decay_distances < 2
        x_cart = (2 - decay_distances[pre_target]) * np.cos(theta_arr[pre_target]) * np.tan(
            phi_arr[pre_target])  # Converting spherical to cartesian
        y_cart = (2 - decay_distances[pre_target]) * np.sin(theta_arr[pre_target]) * np.tan(phi_arr[pre_target])
        x_on_target, y_on_target = get_on_target(x_cart, y_cart, detector_half_size)

        x_smear, y_smear = self._smear(x_cart, y_cart)
        x_smear_on_target, y_smear_on_target = get_on_target(x_smear, y_smear, detector_half_size)

        return OnTarget(x_on_target, y_on_target, x_smear_on_target, y_smear_on_target)

    # Plots a 2d histogram of gamma count against x-y position in detector
    def _hist_2d(self, x: np.array, y: np.array):
        bins = [int(self.detector_size / self.x_res), int(self.detector_size / self.y_res)]
        hist, a, b, c = plt.hist2d(x, y, bins, cmap='magma')
        plt.title('2d histogram of detected gamma rays')
        cbar = plt.colorbar()
        cbar.set_label('Number of counts')
        plt.xlabel('x (m)')
        plt.ylabel('y (m)')
        return hist

    # Shows true distribution of points
    def _jointplot(self, x: np.array, y: np.array):
        df = pd.DataFrame({'x (m)': x, 'y (m)': y})
        sns.jointplot(x='x (m)', y='y (m)', data=df, color='mediumpurple',
                      kind="kde", space=0)
        plt.suptitle('Counts density estimation')
