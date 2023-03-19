Wafer: a class that represents a single wafer, with attributes such as size, thickness, and any other relevant properties.
Batch: a class that represents a batch of wafers, with attributes such as size and a list of the wafers in the batch.
Task: a class that represents a task to be performed on a batch of wafers, with attributes such as processing time and input/output buffers.
Unit: a class that represents a unit in the production line, with attributes such as a list of tasks it can perform and input/output buffers for each task.
ProductionLine: a class that represents the entire production line, with attributes such as a list of units, input/output buffers for the entire line, and a scheduler for managing the order of tasks.
Simulator: a class that simulates the production process by scheduling and executing tasks on the production line.

Each class would have methods for performing various operations on its respective objects, such as loading and unloading batches, assigning input/output buffers, calculating processing times, etc.

The ProductionLine class would also have a method for optimizing the production process by selecting the next batch to treat in one of its input buffers, based on a given heuristic.

The Simulator class would use the scheduler to simulate the production process by loading batches, starting and completing tasks, and updating the completion times of future tasks based on the current state of the production line.
