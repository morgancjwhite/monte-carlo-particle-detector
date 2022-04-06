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
        proportion, cross_sec, index = self._vary_cross()  # mn/mx in nb
        conf_cross = cross_sec[index]
        confidence_arr = proportion * 100  # Converting to percentage
        print(f"The time taken was {perf_counter() - t1}s")

        self._conf_plot(cross_sec, confidence_arr, conf_cross)
        plt.show()

        print('The cross section of particle X is less than', round(conf_cross, 4),
              'nb with', self.confidence, '% confidence')

    # Creates quantity pseudos and calculates proportion above 5 total counts
    def _gen_pseudos(self, cross_section):
        n = 0
        for i in range(self.number_of_pseudos):
            luminosity = self._get_luminosity()
            background = self._background()  # Finding noise and signal counts
            signal = self._signal(cross_section, luminosity)
            if background + signal > 5:  # Seeing if above total counts
                n += 1
        return n / self.number_of_pseudos

    def _get_luminosity(self):
        return abs(np.random.normal(self.luminosity_mean, self.luminosity_std))

    def _background(self):
        # Creates background counts from possion dist. of normally distributed mean
        return np.random.poisson(np.random.normal(self.background_mean, self.background_std))

    def _signal(self, cross_section, luminosity):
        # Creates particle X signal
        return np.random.poisson(luminosity * cross_section)  # From integrated L formula

    # Varies cross section from mn to mx in incr increments
    def _vary_cross(self):
        proportion = np.empty(0)
        cross_sec = np.linspace(self.min_cross_section, self.max_cross_section, self.cross_section_increments)
        m = 0  # Dummy variable
        for j in range(self.cross_section_increments):
            # For each cross section, generate quantity pseudos,
            # see if proportion of counts is above desired confidence
            proportion = np.append(proportion, self._gen_pseudos(cross_sec[j], ))
            # Saves index of first cross_sec to reach desired confidence in array
            if proportion[j] >= (self.confidence/100) and m == 0:
                index = j
                m += 1
        return [proportion, cross_sec, index]

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
