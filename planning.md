# Planning
## Structure
**Wafer:** a class that represents a single wafer, with attributes such as size, thickness, and any other relevant properties.  
**Batch:** a class that represents a batch of wafers, with attributes such as size and a list of the wafers in the batch.  
**Task:** a class that represents a task to be performed on a batch of wafers, with attributes such as processing time and input/output buffers.  
**Unit:** a class that represents a unit in the production line, with attributes such as a list of tasks it can perform and input/output buffers for each task.  
**ProductionLine:** a class that represents the entire production line, with attributes such as a list of units, input/output buffers for the entire line, and a scheduler for managing the order of tasks.  
**Simulator:** a class that simulates the production process by scheduling and executing tasks on the production line.

Each class would have methods for performing various operations on its respective objects, such as loading and unloading batches, assigning input/output buffers, calculating processing times, etc.

The ProductionLine class would also have a method for optimizing the production process by selecting the next batch to treat in one of its input buffers, based on a given heuristic.

The Simulator class would use the scheduler to simulate the production process by loading batches, starting and completing tasks, and updating the completion times of future tasks based on the current state of the production line.

## Questions
1. The assignment states that a unit can only perform one task at a time. Is loading a batch of wafers from the input buffer into a machine a task that belongs to the unit? I belive yes. I will write one example of what i think is a legal production flow and one example of a illegal production flow:

    **Legal flow:** We have a batch of 20 wafers. The unit use one minute to load all the wafers into the machine. The unit use 20*0.5=10 minutes to perform the task on every wafer. The unit uses 1 minute to unload all the wafers out of the machine. A total of 12 minutes at machine 1. 

    **Illegal flow:** We have a batch of 20 wafers. The unit use one minute to load all the wafers into the machine. The unit use 10*0.5=5 minutes to perform the task on the first half of the wafers. Then the unit uses 1 minute to unload the first half. The unit uses 5 minutes to perform the task on the second half of the wafers. Then it uses 1 minutes to unload the second half. Total of 13 minutes on machine 1.

2. The problem with this task is that when a batch is finished its not garanteed that the input buffer on the next machine hase enough place to store the batch. The task states that batches must be unloaded from units as soon as they are processed. If the batch is to big to be placed in the next input buffer then everything stops because our simulation is in a illegal state? Or it is simply blocked until it is space in the input buffer.

