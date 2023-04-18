import heapq
from Batch import Batch, divide_into_most_equal_sized_batches, divide_into_random_sized_batches
from ProductionLine import ProductionLine
from Event import Event 
import matplotlib.pyplot as plt
import random
import csv
class Simulation:

    def try_to_find_new_best_initial_batches_with_genetic_algorithm(self, iterations):
        initial_population = []
        best_time_from_file, initial_batches = self.get_best_initial_batches_from_csv_file("data/best_initial_batches.csv")
       
        for s in range(1000):
            initial_population.append(divide_into_random_sized_batches(1000))

        for i in range(iterations):
            print("generation " + str(i + 1))
            initial_batches_with_time = []
            
            for _ in range(700):
                initial_population.append(divide_into_random_sized_batches(1000))

            for initial_batches in initial_population:
                initial_batches_with_time.append((self.simulate(initial_batches, False), initial_batches))
            
            initial_batches_with_time.sort(key=lambda tup: tup[0])

            
            if initial_batches_with_time[0][0] < best_time_from_file:
                print("New best time found:", initial_batches_with_time[0][0])
                self.save_initial_batches_with_time_as_csv(initial_batches_with_time[0][0], initial_batches_with_time[0][1], "data/best_initial_batches.csv")
            else:
                print("No new best time found:", initial_batches_with_time[0][0], ">", best_time_from_file)

            top_100_mutaded = []
            top_100_org = []

            for tuple in initial_batches_with_time[:100]:
                initial_batches = tuple[1]
                initial_batches_sizes = [batch.size for batch in initial_batches]
                top_100_mutaded.append(self.mutate_list(initial_batches_sizes))
                top_100_org.append(initial_batches_sizes)

            keep = top_100_mutaded + top_100_org
             
            new_gen_initial_batches = [[Batch(index+1, size) for index, size in enumerate(sublist)] for sublist in keep] 
            initial_population = new_gen_initial_batches

    def mutate_list(self, input_list):
        result = input_list.copy()

        # Ensure that index_down is different from index_up
        while True:
            index_up = random.randint(0, len(input_list) - 1)
            index_down = random.randint(0, len(input_list) - 1)

            if index_down == index_up:
                continue
            
            if result[index_up] < 48 and result[index_down] > 22:
                result[index_up] += 3
                result[index_down] -= 3
            else:
                continue
            break
        return result

    def try_to_find_new_best_initial_batches_with_bruteforce(self, iterations):
        best_time = None
        best_initial_batches = None

        for i in range(iterations):
            print("iteration " + str(i + 1))
            initial_batches = divide_into_random_sized_batches(1000)
            
            time = self.simulate(initial_batches, False)
        
            if best_time is None or time < best_time:
                best_time = time
                best_initial_batches = initial_batches
        
        best_time_from_file, initial_batches = self.get_best_initial_batches_from_csv_file("data/best_initial_batches.csv")

        if best_time < best_time_from_file:
            print("New best time found:", best_time)
            self.save_initial_batches_with_time_as_csv(best_time, best_initial_batches, "data/best_initial_batches.csv")
        else:
            print("No new best time found:", best_time, ">", best_time_from_file)

    def save_initial_batches_with_time_as_csv(self, time, inital_batches, file_path):
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            row = [time] + [batch.size for batch in inital_batches]
            writer.writerow(row)
    
    def get_best_initial_batches_from_csv_file(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) == 0:
                return 999999999, None
            
            last_row = rows[-1]
            initial_batches = []
            time = float(last_row[0])
            for i in range(1, len(last_row)):
                initial_batches.append(Batch(i, int(last_row[i])))

            return time, initial_batches

    def simulate(self, initial_batches, print_simulation=True):
        current_time = 0
        load_unload_time = 1
        production_line = ProductionLine()
        
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
                test = unit.unload(current_time, print_simulation)
                if test and print_simulation: 
                   x_values.append(test[0])
                   total_size += test[1]
                   y_values.append(total_size) 
                # We really only need to add a load event for the unit that just unlaoded a task and the unit that got a new batch to one of its input buffers
                # But its easier and dosent hurt to just add a load event for all units
                # If a unit is busy the load event will just try to load the unit and fail
                # If the unload dosent suceed it also dosent hurt to add a load event for all the units
                for unit in production_line.units:
                    event = Event(current_time + load_unload_time, "load", unit)
                    heapq.heappush(event_queue, event)
        
    

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
        
        sum = 0
        for i in production_line.end_buffer.content:
            sum += i.size
        if sum == 1000:
            if print_simulation:
                print("All wafers confirmed in end buffer")
                print("Total time:", current_time)
        else:
            raise Exception("Not all wafers in end buffer")

        return current_time

def main():
    sim = Simulation()
    
    #initial_batches = divide_into_most_equal_sized_batches(1000,37)

    time, initial_batches = sim.get_best_initial_batches_from_csv_file("data/best_initial_batches.csv")

    sim.simulate(initial_batches)

    #sim.try_to_find_new_best_initial_batches_with_bruteforce(1000)
    #sim.try_to_find_new_best_initial_batches_with_genetic_algorithm(100)

if __name__ == '__main__':
    main()