from time import perf_counter
import numpy as np
import matplotlib.pyplot as plt


class Task3:

    def __init__(self, number_of_pseudos):
        self.confidence = 95  # Desired confidence %
        self.number_of_pseudos = number_of_pseudos

        self.min_cross_section = 0  # nb
        self.max_cross_section = 0.8
        self.cross_section_increments = 500

        self.luminosity_std = 0  # Distribution of luminosity
        self.luminosity_mean = 12  # nb-1

        self.background_std = 0.4  # Distribution of background
        self.background_mean = 5.7

    def run(self):
        print('\n\nTask 2: Statistical analysis of Monte Carlo Methods')
        self.stats_of_mcms()

    def stats_of_mcms(self):
        t1 = perf_counter()
        cross_sections, confidences = self._vary_cross_section()
        print(f"The time taken was {perf_counter() - t1}s")

        # Get the 95% confidence cross-section
        confident_cross_section = cross_sections[(confidences > 95).argmax()]
        print(f"Cross section of particle X is less than {round(confident_cross_section, 4)}nb to {self.confidence}%")
        self._conf_plot(cross_sections, confidences, confident_cross_section)
        plt.show()

    def _gen_pseudos(self, cross_section):
        # Creates pseudo experiments and calculate proportion above 5 total counts
        resulting_output = self._background() + self._signal(cross_section)
        return sum(resulting_output > 5) / self.number_of_pseudos

    def _background(self):
        # Creates background counts from possion dist. of normally distributed mean
        gaussian_background = np.random.normal(self.background_mean, self.background_std, self.number_of_pseudos)
        return np.random.poisson(gaussian_background)

    def _signal(self, cross_section) -> np.array:
        # Distribute luminosity then use posisson dist. From integrated L formula
        luminosity = abs(np.random.normal(self.luminosity_mean, self.luminosity_std, self.number_of_pseudos))
        return np.random.poisson(luminosity * cross_section)

    def _vary_cross_section(self):
        # Generate pseudo experiments for increments of a cross section
        cross_sec_iter = np.linspace(self.min_cross_section, self.max_cross_section, self.cross_section_increments)
        confidence_arr = np.array([self._gen_pseudos(cross_sec) for cross_sec in cross_sec_iter])
        return cross_sec_iter, 100 * confidence_arr

    def _conf_plot(self, x, y, conf_cross):
        # Plots confidence interval against cross section and shades confidence area
        fig, ax = plt.subplots()
        plt.plot(x, y)
        plt.xlim(left=0)
        plt.ylim(bottom=min(y))
        plt.xlabel('Cross section of particle X (nb)')
        plt.ylabel('Confidence interval (%)')
        plt.title('Confidence interval versus cross section of particle X')

        # Shading area of confidence
        ax.fill([0, conf_cross, conf_cross, 0], [min(y), min(y), self.confidence, self.confidence],
                color='orange', alpha=0.6)
        plt.hlines(self.confidence, 0, conf_cross, label='95% confidence')
        plt.legend()
