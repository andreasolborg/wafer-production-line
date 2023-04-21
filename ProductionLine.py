# Group 4 - Assignment 3 - Authors: Jon Grendstad, Andreas Blokkum Olborg - TPK4186
import math
from Buffer import Buffer
from Task import Task
from Unit import Unit

class ProductionLine:
    def __init__(self, task_order):
        self.start_buffer = Buffer(1, 120) # We assume the start buffer has infinite capacity
        self.buffer2 = Buffer(2, 120)
        self.buffer3 = Buffer(3, 120)
        self.buffer4 = Buffer(4, 120)
        self.buffer5 = Buffer(5, 120)
        self.buffer6 = Buffer(6, 120)
        self.buffer7 = Buffer(7, 120)
        self.buffer8 = Buffer(8, 120)
        self.buffer9 = Buffer(9, 120)
        self.end_buffer = Buffer(10, math.inf) # We assume the end buffer has infinite capacity

        self.tasks = {
            1: Task(1, 0.5, self.start_buffer, self.buffer2),
            2: Task(2, 3.5, self.buffer2, self.buffer3),
            3: Task(3, 1.2, self.buffer3, self.buffer4),
            4: Task(4, 3.0, self.buffer4, self.buffer5),
            5: Task(5, 0.8, self.buffer5, self.buffer6),
            6: Task(6, 0.5, self.buffer6, self.buffer7),
            7: Task(7, 1.0, self.buffer7, self.buffer8),
            8: Task(8, 1.9, self.buffer8, self.buffer9),
            9: Task(9, 0.3, self.buffer9, self.end_buffer),
        }

        self.unit1 = Unit(1, [self.tasks[task_id] for task_id in task_order[0]])
        self.unit2 = Unit(2, [self.tasks[task_id] for task_id in task_order[1]])
        self.unit3 = Unit(3, [self.tasks[task_id] for task_id in task_order[2]])

        self.units = [self.unit1, self.unit2, self.unit3]
