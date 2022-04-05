from montecarlopd.task_1 import Task1

INVERSE_SAMPLES = 1e4
REJECT_SAMPLES = 1e4

if __name__ == '__main__':
    task_1 = Task1(INVERSE_SAMPLES, REJECT_SAMPLES)
    task_1.run()
