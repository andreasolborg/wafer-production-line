import heapq
from Batch import divide_into_most_equal_sized_batches, divide_into_random_sized_batches, divide_into_increasing_batch_sizes
from ProductionLine import ProductionLine
from Event import Event 
import matplotlib.pyplot as plt
import json #TODO write command on how to install json
from Batch import Batch
import random
class Simulation:



    def try_to_find_new_best_initial_batches_with_genetic_algorithm(self, iterations):
        initial_population = []

        # create 1000 random initial_batches lists
        for s in range(1000):
            initial_population.append(divide_into_random_sized_batches(1000))


        for i in range(iterations):
            initial_batches_with_time = []
            
            for initial_batches in initial_population:
                initial_batches_with_time.append((self.simulate(initial_batches, False), initial_batches))
            
            initial_batches_with_time.sort(key=lambda tup: tup[0])

            print("iteration:",i,",", initial_batches_with_time[0][0])
            #print(i, len(initial_batches_with_time))

            new_gen = []
            old_gen = []
            for tuple in initial_batches_with_time[:100]:
                initial_batches = tuple[1]
                initial_batches_sizes = [batch.size for batch in initial_batches]
                new_gen.append(self.mutate_list(initial_batches_sizes))
            
            for tuple in initial_batches_with_time[:900]:
                initial_batches = tuple[1]
                initial_batches_sizes = [batch.size for batch in initial_batches]
                old_gen.append(initial_batches_sizes)
            
            keep = new_gen + old_gen
            
            new_gen_initial_batches = [[Batch(0, size) for size in sublist] for sublist in keep]   
            initial_population = new_gen_initial_batches

    def mutate_list(self, input_list):
        result = input_list.copy()

        # Ensure that index_down is different from index_up
        while True:
            index_up = random.randint(0, len(input_list) - 1)
            index_down = random.randint(0, len(input_list) - 1)

            if index_down == index_up:
                continue
            
            if result[index_up] < 50 and result[index_down] > 20:
                result[index_up] += 1
                result[index_down] -= 1
            else:
                continue
            break
        return result

    def try_to_find_new_best_initial_batches_with_bruteforce(self, iterations):
        best_time = None
        best_initial_batches = None

        for i in range(iterations):
            print(i)
            initial_batches = divide_into_random_sized_batches(1000)
            
            time = self.simulate(initial_batches, False)
        
            if best_time is None or time < best_time:
                best_time = time
                best_initial_batches = initial_batches
        
        best_time_from_file, initial_batches = self.get_last_batches_from_file("data/best_initial_batches.json")

        print("No new best time found:", best_time, ">", best_time_from_file)

        if best_time < best_time_from_file:
            print("New best time found:", best_time)
            self.save_batch_data_to_file(best_time, best_initial_batches, "data/best_initial_batches.json")

    def get_last_batches_from_file(self, file_path):
        with open(file_path, 'r') as infile:
            file_data = json.load(infile)

        if not file_data:
            print("No data found in the file.")
            return None

        last_data = file_data[-1]  # Get the last JSON object
        batch_list = [Batch(batch['id'], batch['size']) for batch in last_data['initial batches']]
        time = last_data['time']

        return time, batch_list

    def save_batch_data_to_file(self, time, inital_batches, file_path):
        data = {
            "time": time,
            "initial batches": [batch.to_dict() for batch in inital_batches]
        }

        # Check if the file exists and read its content
        try:
            with open(file_path, 'r') as infile:
                file_data = json.load(infile)
        except FileNotFoundError:
            file_data = []

        # Append the new data to the existing content
        file_data.append(data)

        # Save the updated content back to the file
        with open(file_path, 'w') as outfile:
            json.dump(file_data, outfile, indent=4)


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

        return current_time

def main():
    sim = Simulation()
    
    initial_batches = sim.get_last_batches_from_file("data/best_initial_batches.json")[1]
    #initial_batches = divide_into_most_equal_sized_batches(1000,20)
    #initial_batches = divide_into_increasing_batch_sizes()


    #sim.simulate(initial_batches)

    #sim.try_to_find_new_best_initial_batches_with_bruteforce(1000)
    sim.try_to_find_new_best_initial_batches_with_genetic_algorithm(11)

if __name__ == '__main__':
    main()