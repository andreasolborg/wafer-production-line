import numpy as np
import itertools

# Constants and parameters
MIN_WAFER_BATCH = 20
MAX_WAFER_BATCH = 50
BUFFER_CAPACITY = 120
LOAD_UNLOAD_TIME = 1

TASKS = [ # (task_id, processing_time_per_wafer)
    (1, 1.0),
    (2, 2.0),
    (3, 1.5),
    (4, 3.0),
    (5, 2.5),
    (6, 1.0),
    (7, 2.0),
    (8, 1.5),
    (9, 3.0),
]

TARGET_WAFERS = 1000

class Batch:
    def __init__(self, id, num_wafers):
        self.id = id
        self.num_wafers = num_wafers

class WaferProduction:
    def __init__(self):
        self.buffers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.total_wafers = 0
        self.time = 0

    def process_task(self, batch, task_id, task_time):
        self.time += task_time * batch.num_wafers
        self.buffers[task_id] += batch.num_wafers
        print(f"Batch {batch.id} finished Task {task_id} at time {self.time}")

    def load_unload(self):
        self.time += LOAD_UNLOAD_TIME

    def run(self):
        batch_id = itertools.count()
        while self.total_wafers < TARGET_WAFERS:
            num_wafers = np.random.randint(MIN_WAFER_BATCH, MAX_WAFER_BATCH + 1)
            batch = Batch(next(batch_id), num_wafers)

            
            for task_id, (task_num, task_time) in enumerate(TASKS):
                self.load_unload()
                self.process_task(batch, task_num, task_time)
                self.load_unload()

            self.total_wafers += batch.num_wafers
            print(f"Batch {batch.id} completed at time {self.time}")

wafer_production = WaferProduction()
wafer_production.run()

print(f"Total wafers produced: {wafer_production.total_wafers}")