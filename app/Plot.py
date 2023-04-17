import matplotlib.pyplot as plt
from Simulation import Simulation
from Batch import divide_into_most_equal_sized_batches

class Plot:

    def plot_divide_into_most_equal_sized_batches(self):
        sim = Simulation()
        
        x_values = []
        y_values = []

        for i in range(20,51):
            x_values.append(i)
            initital_batches = divide_into_most_equal_sized_batches(1000, i)
            y_values.append(sim.simulate(initital_batches, False))

        plt.plot(x_values, y_values)
        plt.xlabel('average batch sizes')
        plt.ylabel('time until finished')
        plt.title('time until finished for all different average batch sizes')
        plt.show()

    def plot_best_initial_batches(self):
        sim = Simulation()
        initial_batches = sim.get_last_batches_from_file("data/best_initial_batches.json")[1]
        
        x_values = []
        y_values = []

        for i in range(len(initial_batches)):
            x_values.append(i)
            y_values.append(initial_batches[i].size)

        plt.plot(x_values, y_values)
        plt.xlabel('batch number')
        plt.ylabel('batch size')
        plt.title('batch size for every batch number')
        plt.show()

def main():
    plot = Plot()
    plot.plot_divide_into_most_equal_sized_batches()
    plot.plot_best_initial_batches()

main()