from montecarlopd.task_1 import Task1
from montecarlopd.task_2 import Task2

# Task 1
INVERSE_SAMPLES = 1e4
REJECT_SAMPLES = 1e4

# Task 2
# How many random decays in task 2
PARTICLE_SAMPLES = 1e5

# Total detector length (square detector)

if __name__ == '__main__':
    # Task 1
    # Inverse and rejection sampling of a sine curve
    task_1 = Task1(INVERSE_SAMPLES, REJECT_SAMPLES)
    task_1.run()

    # Task 2
    # Inverse and rejection sampling of a sine curve
    task_2 = Task2(PARTICLE_SAMPLES)
    task_2.run()
