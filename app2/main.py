import heapq

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
        if self.get_total_wafers() + batch.size <= self.capacity:
            self.content.append(batch)
            return True
        else:
            print(batch, " is gone, was unloaded, but no space in outputbuffer")

    def remove_batch(self):
        if self.content:
            return self.content.pop(0)
        return None

    def get_total_wafers(self):
        return sum(batch.size for batch in self.content)

class Task:
    def __init__(self, id, time_per_wafer, inputbuffer, outputbuffer):
        self.id = id
        self.time_per_wafer = time_per_wafer
        self.inputbuffer = inputbuffer
        self.outputbuffer = outputbuffer

        self.batch_in_task = None

    def load(self, current_tick):
        self.batch_in_task = self.inputbuffer.remove_batch()
        if self.batch_in_task:  # Check if there's a batch to process
            locked_to_tick = self.batch_in_task.size * self.time_per_wafer + current_tick
            print("tick:", current_tick, "---", self, "batch", self.batch_in_task.id, "loaded and finishes at", locked_to_tick)
            return locked_to_tick
        return False  # It should be a batch to process but we return False and checks it in the unit to be sure

    def unload(self, current_tick):
        if self.batch_in_task:
            if self.outputbuffer.add_batch(self.batch_in_task):
                print("tick:", current_tick, "---", self, "batch", self.batch_in_task.id, "unloaded")
                self.batch_in_task = None
                return True
           
    def __str__(self):
        return "task" + str(self.id)


class Unit:
    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks
        self.locked_to_tick = 0

    def load(self, current_tick):
        # Check if the unit is locked to a ongoing task
        if current_tick >= self.locked_to_tick:
            return self.choose_next_task(current_tick)
        # We return false if we dont find any task with something in the input buffer
        return False

    def unload(self, current_tick): 
        # When we unload we find the first task in the unit with a active batch and unload it
        # A unit will never have two tasks with a active batch at the same time, since its illegal
        for task in self.tasks:
            if task.batch_in_task:
                return task.unload(current_tick)


    # This is the method implemented for choosing the next task for now
    def choose_next_task(self, current_tick):
        # We simply take the first task in the unit that has something in the input buffer
        for task in self.tasks:
            if task.inputbuffer.content:
                locked_to_tick = task.load(current_tick)
                if locked_to_tick:
                    self.locked_to_tick = locked_to_tick
                    return True

    def __str__(self):
        return "unit" + str(self.id)

class ProductionLine:
    def __init__(self):
        start_buffer = Buffer(999999)
        buffer2 = Buffer(1200)
        buffer3 = Buffer(1200)
        buffer4 = Buffer(1200)
        buffer5 = Buffer(1200)
        buffer6 = Buffer(1200)
        buffer7 = Buffer(1200)
        buffer8 = Buffer(1200)
        buffer9 = Buffer(1200)
        end_buffer = Buffer(999999)

        task1 = Task(1, 0.5, start_buffer, buffer2)
        task2 = Task(2, 3.5, buffer2, buffer3)
        task3 = Task(3, 1.2, buffer3, buffer4)
        task4 = Task(4, 3.0, buffer4, buffer5)
        task5 = Task(5, 0.8, buffer5, buffer6)
        task6 = Task(6, 0.5, buffer6, buffer7)
        task7 = Task(7, 1.0, buffer7, buffer8)
        task8 = Task(8, 1.9, buffer8, buffer9)
        task9 = Task(9, 0.3, buffer9, end_buffer)

        unit1 = Unit(1, [task1, task3, task6, task9])
        unit2 = Unit(2, [task2, task5, task7])
        unit3 = Unit(3, [task4, task8])

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

def print_event_queue(event_queue):
    for event in event_queue:
        print(event, end=" ")
    print()

class Simulation:
    def simulate(self):
        current_tick = 0

        initial_batches = [Batch(20, 1), Batch(30, 2), Batch(50, 3), Batch(40, 4), Batch(20, 5)]

        production_line = ProductionLine()

        # Add initial batches to start buffer
        for batch in initial_batches:
            production_line.buffers[0].add_batch(batch)

        event_queue = []

        # Start the simulation by adding a load event for each unit
        for unit in production_line.units:
            event = Event(current_tick, "load", unit)
            # heappush is the same as append
            # heappop is the same as pop(0)
            # the different between a heapq and a list is that at any given time the first element is going to be the minimum element
            # the heapq is sorted on time, see "__lt__" function in Event class
            heapq.heappush(event_queue, event)

        # Keep the simulation going as long as there is events in the event queue
        while event_queue:
            #print_event_queue(event_queue)
            # heappop will always remove the first element in the list, wich is the event with the lowest tick
            event = heapq.heappop(event_queue)

            current_tick = event.time
            unit = event.unit

            # If the event action is load we try to load the unit and if we succeed we add an unload event to a calculated future tick
            if event.action == "load":
                if unit.load(current_tick):
                    event = Event(unit.locked_to_tick + 1, "unload", unit)
                    heapq.heappush(event_queue, event)

            # If the event action is unload we try to unload the unit and if we succeed we add a load event to the event queue
            elif event.action == "unload":
                unit.unload(current_tick)
                # We really just need to call a new load event on the unit that just was unloaded and the unit that just got its inputbuffer loaded with the unloaded batch
                # But it it dosent hurt to add a load event for all units, and its easier to implement
                # The load event on the third unit will just dissapear if the unit is busy anyways
                for unit in production_line.units:
                    event = Event(current_tick + 1, "load", unit)
                    heapq.heappush(event_queue, event)


            # If a load event cant go trough because a unit is busy the event gets removed from the queue
            # This is not a problem because a new load event will be added to the queue when the unit is done with its locked task
            # Then the first item in the buffer will be loaded   


def main():
    sim = Simulation()
    sim.simulate()


main()