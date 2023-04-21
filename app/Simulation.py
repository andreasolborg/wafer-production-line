import heapq
from Batch import Batch, divide_into_most_equal_sized_batches, divide_into_random_sized_batches
from ProductionLine import ProductionLine
from Event import Event 
import matplotlib.pyplot as plt
import random
import csv
import itertools
import copy

AMOUNT_OF_WAFERS = 1000
class Simulation:

    def try_to_find_new_best_initial_batches_with_genetic_algorithm(self, generations, task_prioritization):
        print("## FINDING BEST INITIAL BATCHES WITH GENETIC ALGORITHM ##")
        
        best_time_from_file, initial_batches_from_file, task_prioritization_from_file = self.get_best_initial_batches_with_time_and_task_prioritization_from_csv_file("data/best_initial_batches.csv")
        
        initial_population = []
        
        # We want to take all our best initial batches and add them to the population
        all_initial_batches_from_file = self.get_all_initial_batches_from_csv_file("data/best_initial_batches.csv")
        
        # We create 400 random initial batches and add them to the population
        for _ in range(500):
            initial_population.append(divide_into_random_sized_batches(AMOUNT_OF_WAFERS))
        
        
        initial_population.extend(all_initial_batches_from_file)

        for i in range(generations):
            print("----- Generation " + str(i + 1), "-----")

            initial_batches_and_their_simulation_time = []
            
            # We want to add 800 new random initial batches to the population since we only keep the 10% mutated and the 10% best original
            for _ in range(800):
                initial_population.append(divide_into_random_sized_batches(AMOUNT_OF_WAFERS))
            
            # We want to simulate all the initial batches in the population and add them to a list with their time
            for initial_batches in initial_population:

                initial_batches_and_their_simulation_time.append((self.simulate(initial_batches, task_prioritization , False), initial_batches))
            
            # We sort the list by time
            initial_batches_and_their_simulation_time.sort(key=lambda tup: tup[0])

            

            # If the best time is better than the best time from the file we save it to the file
            if initial_batches_and_their_simulation_time[0][0] < best_time_from_file:
                print("New best time found:   ", initial_batches_and_their_simulation_time[0][0])
                best_time_from_file = initial_batches_and_their_simulation_time[0][0]
                self.save_initial_batches_with_time_and_task_task_prioritization_as_csv(initial_batches_and_their_simulation_time[0][0], initial_batches_and_their_simulation_time[0][1], task_prioritization, "data/best_initial_batches.csv")
            else:
                print("No new best time found:", initial_batches_and_their_simulation_time[0][0], ">=", best_time_from_file)
                print("Best initial batches this generation:", [batch.size for batch in initial_batches_and_their_simulation_time[0][1]])


            top_100_mutaded = []
            top_100_original = []
            
            print("Current top 10:        ", end=" ")
            for i,tuple in enumerate(initial_batches_and_their_simulation_time[:100]):
                if i < 10:
                    print(tuple[0], end=" ")
                initial_batches = tuple[1]
                top_100_original.append(initial_batches)
                top_100_mutaded.append(self.mutate_initial_batches(initial_batches))
            print()     
            keep_in_next_generation = top_100_mutaded + top_100_original

            initial_population = keep_in_next_generation
        print()

    def mutate_initial_batches(self, initial_batches):
        result = copy.deepcopy(initial_batches)

        while True:
            index_up = random.randint(0, len(initial_batches) - 1)
            index_down = random.randint(0, len(initial_batches) - 1)

            if index_down == index_up:
                continue

            batch_to_size_up = result[index_up]
            batch_to_size_down = result[index_down]

            if batch_to_size_down.size > 20 and batch_to_size_up.size < 50:
                batch_to_size_up.size += 1
                batch_to_size_down.size -= 1
            else:
                continue
            break

        return result

    def try_to_find_new_best_initial_batches_with_bruteforce(self, iterations, task_prioritization):
        print("## FINDING BEST INITIAL BATCHES WITH BRUTEFORCE ##")
        best_time_from_file, initial_batches_from_file, task_prioritization_from_file = self.get_best_initial_batches_with_time_and_task_prioritization_from_csv_file("data/best_initial_batches.csv")
        
        best_time = None
        best_initial_batches = None

        for i in range(iterations):
            print("----- Iteration " + str(i + 1) + " -----")
            initial_batches = divide_into_random_sized_batches(AMOUNT_OF_WAFERS)
            
            time = self.simulate(initial_batches, task_prioritization, False)
        
            if best_time is None or time < best_time:
                best_time = time
                best_initial_batches = initial_batches

        if best_time < best_time_from_file:
            print("New best time found:   ", best_time)
            self.save_initial_batches_with_time_and_task_task_prioritization_as_csv(best_time, best_initial_batches, task_prioritization, "data/best_initial_batches.csv")
        else:
            print("No new best time found:", best_time, ">=", best_time_from_file)
        
        print()


    def try_all_task_prioritization(self, initial_batches):
        print("## FINDING BEST TASK PRIORITIZATION BY TRYING ALL PERMUTATIONS ##")
        def combine_lists(lists, current_combination=[]):
            if not lists:
                yield current_combination 
                return
            for element in itertools.permutations(lists[0]):
                yield from combine_lists(lists[1:], current_combination + list(element))

        tasks = [[1, 3, 6, 9], [2, 5, 7], [4, 8]]
        best_time = None
        best_permutation = None
        result = list(combine_lists(tasks))
        sim = Simulation()
        
        for i, r in enumerate(result):
            
            task_prioritization = [[r[0], r[1], r[2], r[3]], [r[4], r[5], r[6]], [r[7], r[8]]]
            time = sim.simulate(initial_batches, task_prioritization, False)
            print("Permutation number " + str(i) + ": " + str(task_prioritization) + ", time = " + str(time))
          
            
            if best_time is None or time < best_time:
                best_time = time
                best_permutation = task_prioritization

        print("Best permutation      : " + str(best_permutation) + ", time = " + str(best_time))
        print()

    # The csv format:
    # 1,3,6,9,5,7,2,4,8,5591.6,20,20,35,27,21,22,32,34,45,37,40,25,20,38,33,27,27,42,21,28,33,38,29,24,23,22,28,24,22,32,29,20,20,21,21,20
    # The frirst 10 numbers are the task order, the next number is the time, and the rest are the initial batch sizes
    def save_initial_batches_with_time_and_task_task_prioritization_as_csv(self, time, inital_batches, task_order, file_path):
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            row = list(itertools.chain.from_iterable(task_order)) + [time] + [batch.size for batch in inital_batches]
            writer.writerow(row)
    
    def get_all_initial_batches_from_csv_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) == 0:
                return None
            all_initial_batches = []
            for row in rows:
                initial_batches = []
                for i in range(10, len(row)):
                    initial_batches.append(Batch(i-9, int(row[i])))
                all_initial_batches.append(initial_batches)

            return all_initial_batches

    def get_best_initial_batches_with_time_and_task_prioritization_from_csv_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) == 0:
                return 999999999, None
            
            last_row = rows[-1]
            initial_batches = []
            time = float(last_row[9])
            task_order = [[int(last_row[0]), int(last_row[1]), int(last_row[2]), int(last_row[3])], [int(last_row[4]), int(last_row[5]), int(last_row[6])], [int(last_row[7]), int(last_row[8])]]
            for i in range(10, len(last_row)):
                initial_batches.append(Batch(i-9, int(last_row[i])))

            return time, initial_batches, task_order
        
    def simulate(self, initial_batches, task_prioritization, print_simulation=True):
        
        if print_simulation:
            print("## SIMULATING ONE CASE WITH PRINT ##")


        current_time = 0
        load_unload_time = 1
        production_line = ProductionLine(task_prioritization)
        

        # Add initial batches to start buffer
        for batch in initial_batches:
            production_line.start_buffer.add_batch(batch)

        event_queue = []

        x_values = []
        y_values = []
        total_size = 0

        # Start the simulation by adding a load event for the first unit that has the first task
        event = Event(current_time + load_unload_time, "load", production_line.unit1)
        # heappush works the same as append for a list
        # heappop works the same as pop(0) for a list
        # the different between a heapq and a list is that at any given time the first element is going to be the minimum element
        # the heapq is sorted on the attribute time
        heapq.heappush(event_queue, event)


        #for i in range(len(initial_batches)):
        #    event = Event(0, "load_to_start_buffer", None)
        #    heapq.heappush(event_queue, event)
#

        # we keep the simulation going as long as there is events in the event queue
        while event_queue:
            event = heapq.heappop(event_queue)
            
            current_time = event.time
            unit = event.unit

            # If the event action is load we try to load the unit and if we succeed we add an unload event to a calculated future tick based on the task processing time and the batch size
            if event.action == "load":
                if unit.load(current_time, production_line, print_simulation):
                    event = Event(unit.time_until_finished + load_unload_time, "unload", unit)
                    heapq.heappush(event_queue, event)


            # If the event action is unload we unload the task in the unit and add load events for all the units
            elif event.action == "unload":
                # This will only return a size if it was unloaded in the end buffer
                size_unloaded_in_end_buffer = unit.unload(current_time, print_simulation)
                if size_unloaded_in_end_buffer: 
                   x_values.append(current_time)
                   total_size += size_unloaded_in_end_buffer
                   y_values.append(total_size) 
                # We really only need to add a load event for the unit that just unlaoded a task and the unit that got a new batch to one of its input buffers
                # But its easier and dosent hurt to just add a load event for all units
                # If a unit is busy the load event will just try to load the unit and fail
                # If the unload dosent suceed it also dosent hurt to add a load event for all the units
                for unit in production_line.units:
                    event = Event(current_time + load_unload_time, "load", unit)
                    heapq.heappush(event_queue, event)
            
            #elif event.action == "load_to_start_buffer":
            #    batch_to_be_popped = initial_batches[0]
            #    print(batch_to_be_popped)
            #    if production_line.start_buffer.add_batch(batch_to_be_popped):
            #        print("JA")
            #        initial_batches.pop(0)
            #        for unit in production_line.units:
            #            event = Event(current_time + load_unload_time, "load", unit)
            #            heapq.heappush(event_queue, event)
            #    else: 
            #        print("IKKE")
            #        event = Event(current_time + 1, "load_to_start_buffer", None)
            #        heapq.heappush(event_queue, event)
#
#

        if print_simulation:
            fig,ax = plt.subplots()
            ax.plot(x_values,y_values)
            xticks = [x_values[len(x_values)//2], x_values[-1]]
            yticks = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
            ax.set_xticks(xticks)

            ax.set_yticks(yticks)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            plt.show()
            plt.close()
        
        if total_size == AMOUNT_OF_WAFERS:
            if print_simulation:
                with open("simulation.tsv", "a") as file:
                    file.write(str(current_time) + "\tNone\tNone\tComplete\t"+str(current_time))
                print("All wafers confirmed in end buffer")
                print("Total time:", current_time)
        else:
            raise Exception("Not all wafers in end buffer")
        
        if print_simulation:
            print()

        return current_time

def main():
    sim = Simulation()
    
    #clear simulation.tsv file
    file = open("simulation.tsv", "w")
    file.close()
    

    time, initial_batches, task_prioritization = sim.get_best_initial_batches_with_time_and_task_prioritization_from_csv_file("data/best_initial_batches.csv")
    #initial_batches = divide_into_most_equal_sized_batches(1000, 20)

    sim.simulate(initial_batches, task_prioritization, True)
    # sim.try_all_task_prioritization(initial_batches)
    # sim.try_to_find_new_best_initial_batches_with_bruteforce(100, task_prioritization)
    # sim.try_to_find_new_best_initial_batches_with_genetic_algorithm(3, task_prioritization)

if __name__ == '__main__':
    main()