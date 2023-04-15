import heapq
from Batch import Batch
from ProductionLine import ProductionLine
from Event import Event 

import random

class Simulation:
    def simulate(self):
        current_time = 0
        load_unload_time = 1


        # make batches of size between 20 and 70 for a total of 1000 batches
        initial_batches = []
        size_of_batches = 0
        id = 0
        while size_of_batches < 1000:
            id += 1
            batch_size = random.randint(20, 70)
            size_of_batches += batch_size
            initial_batches.append(Batch(batch_size, id))

        for batch in initial_batches:
            print(batch)

        


        production_line = ProductionLine()

        # Add initial batches to start buffer
        for batch in initial_batches:
            production_line.start_buffer.add_batch(batch)

        event_queue = []

        # Start the simulation by adding a load event for the first unit that has the first task
        event = Event(current_time + load_unload_time, "load", production_line.unit1)
        # heappush works the same as append for a list
        # heappop works the same as pop(0) for a list
        # the different between a heapq and a list is that at any given time the first element is going to be the minimum element
        # the heapq is sorted on the attribute time
        heapq.heappush(event_queue, event)

        # we keep the simulation going as long as there is events in the event queue
        while event_queue:
            # print_event_queue(event_queue)
            event = heapq.heappop(event_queue)

            current_time = event.time
            unit = event.unit

            # If the event action is load we try to load the unit and if we succeed we add an unload event to a calculated future tick based on the task processing time and the batch size
            if event.action == "load":
                if unit.load(current_time, production_line):
                    event = Event(unit.time_until_finished + load_unload_time, "unload", unit)
                    heapq.heappush(event_queue, event)

            # If the event action is unload we unload the task in the unit and add load events for all the units
            elif event.action == "unload":
                unit.unload(current_time)
                # We really only need to add a load event for the unit that just unlaoded a task and the unit that got a new batch to one of its input buffers
                # But its easier and dosent hurt to just add a load event for all units
                # If a unit is busy the load event will just try to load the unit and fail
                # If the unload dosent suceed it also dosent hurt to add a load event for all the units
                for unit in production_line.units:
                    event = Event(current_time + load_unload_time, "load", unit)
                    heapq.heappush(event_queue, event)

def print_event_queue(event_queue):
    for event in event_queue:
        print(event, end=" ")
    print()

def main():
    sim = Simulation()
    sim.simulate()

main()