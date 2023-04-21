import matplotlib.pyplot as plt
from Simulation import Simulation
from Batch import divide_into_most_equal_sized_batches

class Plot:

    def plot_divide_into_most_equal_sized_batches(self):
        sim = Simulation()
        task_prioritization = [[1, 3, 6, 9], [5, 7, 2], [4, 8]] 
        x_values = []
        y_values = []

        for i in range(20,51):
            x_values.append(i)
            initital_batches = divide_into_most_equal_sized_batches(1000, i)
            y_values.append(sim.simulate(initital_batches, task_prioritization, 6,False))

        plt.plot(x_values, y_values)
        plt.xlabel("Average batch size")
        plt.ylabel("Simulation time")
        plt.title("1000 wafers splitted into most equal batch sizes possible and their simulation time")
        plt.show()

    def plot_best_initial_batches(self):
        sim = Simulation()
        time, initial_batches, task_prioritization, timeout = sim.get_best_initial_batches_with_time_and_task_prioritization_and_timeout_from_csv_file("data/best_initial_batches.csv")
        
        x_values = []
        y_values = []

        for i in range(len(initial_batches)):
            x_values.append(i)
            y_values.append(initial_batches[i].size)

        plt.plot(x_values, y_values)
        plt.xlabel('Batch number')
        plt.ylabel('Batch size')
        plt.title('Batch size for every batch number')
        plt.show()


def main():
    plot = Plot()
    plot.plot_divide_into_most_equal_sized_batches()
    plot.plot_best_initial_batches()

main()