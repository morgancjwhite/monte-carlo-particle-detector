from montecarlopd.task_1 import Task1
from montecarlopd.task_2 import Task2

# Task 1
from montecarlopd.task_3 import Task3

INVERSE_SAMPLES = 1e4
REJECT_SAMPLES = 1e4

# Task 2
# - Number of particles modeled
PARTICLE_SAMPLES = 1e5

# Task 3
# - Number of pseudo-experiments per cross-section
PSEUDO_EXPERIMENTS = int(5e3)


if __name__ == '__main__':
    # Task 1
    # Inverse and rejection sampling of a sine curve
    task_1 = Task1(INVERSE_SAMPLES, REJECT_SAMPLES)
    task_1.run()

    # Task 2
    # # Inverse and rejection sampling of a sine curve
    task_2 = Task2(PARTICLE_SAMPLES)
    task_2.run()

    # Task 3
    # # Statistical Analysis of Monte Carlo methods
    task_3 = Task3(PSEUDO_EXPERIMENTS)
    task_3.run()
