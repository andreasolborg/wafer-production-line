# Code Documentation

## Proposed solution for each task

### Task 1
We've designed the following classes for the task: Batch, Buffer, Task, Unit, and ProductionLine
- #### Batch:
    - Attributes:
        - size: Represents the number of wafers in a batch.
        - id: Used for printing the process.
        - Initialization: All attributes are set using arguments.
    Buffer:
    - Attributes:
        - capacity: Represents the maximum wafers it can hold.	
        - content: List of batches currently in the buffer.
        - id: Used for printing the process.
    - Functions:
        - add_batch: Insert a batch into the buffer.
        - remove_batch: Remove a batch from the buffer.
        - get_total_wafers: Calculate the total wafers in the buffer
    - Initialization: id and capacity are set using arguments.

- #### Task:
    - Attributes:
        - inputbuffer: where the task receives batches.
        - outputbuffer: where the task sends processed batches.
        - time_per_wafer: time required to process a single wafer.
        - active_batch: batch being processed by the task.
        - id: used for printing the process.
    - Functions:
        - load: insert a batch into the task.
        - unload: remove a batch from the task.
        - check_if_output_buffer_space: verify if there's enough space in the output buffer to load a batch.
        - Initialization: inputbuffer, outputbuffer and time_per_wafer are set using arguments.

- #### Unit:
    - Attributes:
        - tasks: a list of the task in prioritized order.
        - time_unitil_finished: is a timestamp into the future on how long until the unit is free and can take a new task.
    - Functions:
        - load: This function will call the the load function of the next task if the current time is bigger than the time_until_finished attribute.
        - Unload: This function will unload the finished task in the unit.
        - choose_next_task: Finds the first next task with a batch in the inputbuffer in the list of tasks.
    - Initialization: id and tasks are set using arguments.

- #### ProductionLine:
    - Attributes:
        - We have an attribute for each buffer, each task, and each unit.
    - Initialization: Takes in a 2d list of all the task prioritized for the different units
    - Functions:
        - The only function we have is the initialization function that initializes the production line.

### Task 2
The printer we implemented is very simple. We have a print statement that only prints when a task is sucessfully loaded. The logged information is timestamp (tick), task id, batch id (the batch that was loaded), and task completion time. We have a print statement that only prints when a task is sucessfully unloaded. The logged information is timestamp, task id and batch id. We also have a print statement that prints when it has checked that no batch was lost during the simulation. And we have a final printstatement that prints the final simulation time.

### Task 3
To solve this task we have created a discrete event simulator (DES). A discrete event simulator is a computational tool that models the behavior of a system by simulating discrete events over time, capturing changes in state, and evaluating performance metrics.

We've designed the following classes for the task: Event and Simulation. We also use a heapq for scheduling the events.

- #### Event:
    - Attributes:
        - time: Represent the time when the event is going to take place
        - action: Represent what action the event is going to trigger
        - unit: Represen what unit is going to perform the action
    - fucntions:
        - __lt__: This function implements "less than comparison" between two objects of this class. 

- #### Simulation:
    - function:
        - simulate: This is our simulation loop

- #### heapq
    - We use the heapq to always have our events sorted so the event with the lowest timestamp will always be fired first.
    - heappush works the same as append for a list.
    - heappop works the same as pop(0) for a list.
    - the different between a heapq and a list is that at any given time the first element is going to be the minimum element.
    - the heapq is sorted on the attribute time because of the __lt__ function we created in the Event class.

Our event has two types of actions:
- load: a load event will always add a unload event to the event_queue with the timestamp for when the task is done processing\
- unload: a unload event will always add a load event for the unit that was unloaded and the unit that had one of its buffers loaded with a new batch

A load event is only going to be sucessfull if a unit is free and can take a new task. If its not free when the load event occurs it will simply remove it from the event_queue. This is fine and a new load event will be created when the unit has unloaded and is free. A unload event is never going to fail since we have functionality to only load a unit if its possible to unload it when the task is done processing. If a unload event fails our whole system collapses and we loose batches in the production line.

Our simulate function takes in the following parameters: initial_batches (the 1000 wafers splitted into batches), task_prioritization (a 2d list of the task prioritized) and print_simulation (boolean for printing or not). The first that happens in our funtion is that we add the initial batches to the first buffer. We gave this buffer infinity capacaty since the simulation time was not going to get affected by it. So when all the buffers are loaded to the first buffer we start the simulation by adding a load event for the first unit that has the first task. We then go into a loop that runs while the event_queue has event in it. This list is always sorted by our heapq functionality. Since a load event will add a unload event to the event_queue and a unload event will add a load event to the event_queue our simulation will run until all batches are in the end buffer. The end buffer also has infite capacity. We can then check the time when the simualtion stopped and know how long it took.

### Task 4
The simulation is written to a tsv file, and works by writing a line everytime an Action/Event is triggered on a Task object. The file is called simulation.tsv and is located in the data folder.