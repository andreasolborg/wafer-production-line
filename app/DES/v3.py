import heapq
import random


class Batch:
    def __init__(self, size, id):
        self.id = id
        self.size = size

    def __str__(self):
        return "batch" + str(self.id)


class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.content = []

    def add_batch(self, batch):
        if sum(batch.size for batch in self.content) + batch.size <= self.capacity:
            self.content.append(batch)
            return True
        return False

    def remove_batch(self):
        if self.content:
            return self.content.pop(0)
        return None

    def get_amount(self):
        return sum(batch.size for batch in self.content)


class Task:
    def __init__(self, time_per_wafer, inputbuffer, outputbuffer, id):
        self.id = id
        self.batch_in_task = None
        self.inputbuffer = inputbuffer
        self.outputbuffer = outputbuffer
        self.time_per_wafer = time_per_wafer

    def load(self, current_tick):
        self.batch_in_task = self.inputbuffer.remove_batch()
        if self.batch_in_task:  # Check if there's a batch to process
            self.locked_to = self.batch_in_task.size * self.time_per_wafer + current_tick
            print("tick:", current_tick, "---", self, "batch", self.batch_in_task.id, "is finished at", self.locked_to)
            return self.locked_to
        return None  # Return None if there's no batch to process

    def unload(self, current_tick):
        if self.batch_in_task:
            self.outputbuffer.add_batch(self.batch_in_task)
            self.batch_in_task = None

    def __str__(self):
        return "task" + str(self.id)


class Unit:
    def __init__(self, tasks, id):
        self.id = id
        self.tasks = tasks
        self.locked_to_tick = 0

    def load(self, current_tick):
        if current_tick >= self.locked_to_tick:
            for task in self.tasks:
                if task.inputbuffer.content:
                    locked_to_tick = task.load(current_tick)
                    if locked_to_tick:
                        self.locked_to_tick = locked_to_tick
                        return True
        return False

    def unload(self, current_tick):  # Added current_tick parameter
        for task in self.tasks:
            if task.batch_in_task:
                task.unload(current_tick)
                return True

    def __str__(self):
        return "unit" + str(self.id)


class ProductionLine:
    def __init__(self):
        start_buffer = Buffer(999999)
        buffer2 = Buffer(999999)
        buffer3 = Buffer(999999)
        buffer4 = Buffer(999999)
        buffer5 = Buffer(999999)
        buffer6 = Buffer(999999)
        buffer7 = Buffer(999999)
        buffer8 = Buffer(999999)
        buffer9 = Buffer(999999)
        end_buffer = Buffer(999999)

        task1 = Task(0.5, start_buffer, buffer2, 1)
        task2 = Task(3.5, buffer2, buffer3, 2)
        task3 = Task(1.2, buffer3, buffer4, 3)
        task4 = Task(3.0, buffer4, buffer5, 4)
        task5 = Task(0.8, buffer5, buffer6, 5)
        task6 = Task(0.5, buffer6, buffer7, 6)
        task7 = Task(1.0, buffer7, buffer8, 7)
        task8 = Task(1.9, buffer8, buffer9, 8)
        task9 = Task(0.3, buffer9, end_buffer, 9)

        unit1 = Unit([task1, task3, task6, task9], 1)
        unit2 = Unit([task2, task5, task7], 2)
        unit3 = Unit([task4, task8], 3)

        self.units = [unit1, unit2, unit3]
        self.buffers = [start_buffer, buffer2, buffer3, buffer4, buffer5, buffer6, buffer7, buffer8, buffer9, end_buffer]


class Event:
    def __init__(self, time, action, unit):
        self.time = time
        self.action = action
        self.unit = unit

    def __lt__(self, other_event):
        return self.time < other_event.time

    def __str__(self):
        return "[" + str(self.time) + "|" + str(self.action) + "|" + str(self.unit) + "]"


class Simulation:
    def simulate(self):
        current_tick = 0

        initial_batches = [Batch(20, 1), Batch(30, 2), Batch(50, 3), Batch(40, 4), Batch(20, 5)]

        production_line = ProductionLine()

        for batch in initial_batches:
            production_line.buffers[0].add_batch(batch)

        event_queue = []

        for unit in production_line.units:
            event = Event(current_tick, "load", unit)
            heapq.heappush(event_queue, event)

        while event_queue:
            event = heapq.heappop(event_queue)

            current_tick = event.time
            unit = event.unit

            if event.action == "load":
                if unit.load(current_tick):
                    event = Event(unit.locked_to_tick, "unload", unit)
                    heapq.heappush(event_queue, event)

            elif event.action == "unload":
                unit.unload(current_tick)  # Added current_tick
                for unit in production_line.units:
                    event = Event(current_tick, "load", unit)
                    heapq.heappush(event_queue, event)


def main():
    sim = Simulation()
    sim.simulate()


main()