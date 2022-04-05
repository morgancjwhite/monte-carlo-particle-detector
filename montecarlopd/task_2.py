
class Task2:
    def __init__(self):
        x_res = 0.1 #resolution of the detector
        y_res = 0.3
        pass

    def run(self):
        self.particle_decay_mcm()
        pass

    def particle_decay_mcm(self):
        [phi, theta] = gen_angles(n_detec)
        [x_smear, y_smear, x, y] = gen_xy(decay_distance(2000, n_detec), theta, phi, detec_size / 2, n_detec)

        print('Here is a 2d histogram and a jointplot for the unsmeared detector')
        hist = hist_2d(x, y)
        jointplot(x, y)
        plt.show()

        print('Here is a 2d histogram and a jointplot for the smeared detector')
        hist_smear = hist_2d(x_smear, y_smear)
        jointplot(x_smear, y_smear)
        plt.show()

    # Generates angles
    def gen_angles(self, n):
        phi = np.arccos(1 - np.random.uniform(0, 1, n))  # Polar [0, pi/2]
        theta = np.random.uniform(0, 2 * np.pi, n)  # Azimuth [0, 2pi]
        return [phi, theta]

    # Creates array of decay distances using poission dist.
    def decay_distance(self, v, n):
        t = np.random.exponential(550e-6, n)  # Decay times, mean 550 microseconds
        return v * t  # Multiplying by velocity of particle gives decay distance

    # Smears result with gaussian with standard deviation of resolution
    def smear(self, x, y, x_bin, y_bin):
        x = np.random.normal(x, x_bin)
        y = np.random.normal(y, y_bin)
        return [x, y]

        # Converts speherical co-ords into cartesian on xy plane

    def gen_xy(self, d, theta, phi, detec_size, n):
        x = np.empty(0)
        y = np.empty(0)
        x_un = np.empty(0)
        y_un = np.empty(0)
        for i in range(n):
            # Converting spherical to cartesian
            if d[i] < 2:  # Removing all photons that missed the detector
                x_new = (2 - d[i]) * np.cos(theta[i]) * np.tan(phi[i])
                y_new = (2 - d[i]) * np.sin(theta[i]) * np.tan(phi[i])
                if abs(x_new) < detec_size and abs(y_new) < detec_size:
                    x_un = np.append(x_un, x_new)  # Unsmeared
                    y_un = np.append(y_un, y_new)
                [x_smear, y_smear] = smear(x_new, y_new, x_res, y_res)
                if abs(x_smear) < detec_size and abs(y_smear) < detec_size:
                    x = np.append(x, x_smear)  # Smeared
                    y = np.append(y, y_smear)
        return [x, y, x_un, y_un]
