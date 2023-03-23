class Batch:
    def __init__(self, size):
        self.size = size
        self.processing_times = [0, 0, 0, 0, 0, 0, 0, 0, 0] # time for 
        self.current_task = 1
    
    def get_processing_time(self):
        return self.processing_times[self.current_task - 1] * self.size
    
    def increment_task(self):
        self.current_task += 1
        
    def is_done(self):
        return self.current_task == 10

class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.batches = []
        
    def is_full(self):
        return sum([batch.size for batch in self.batches]) == self.capacity
        
    def is_empty(self):
        return len(self.batches) == 0
        
    def add_batch(self, batch):
        if not self.is_full():
            self.batches.append(batch)
            
    def remove_batch(self):
        if not self.is_empty():
            return self.batches.pop(0)
        else:
            return None
        
class Task:
    def __init__(self, task_number, input_buffer, output_buffer):
        self.task_number = task_number
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer
        self.current_batch = None
        
    def is_busy(self):
        return self.current_batch is not None
        
    def has_room(self, batch_size):
        return sum([batch.size for batch in self.output_buffer.batches]) + batch_size <= self.output_buffer.capacity
    
    def next_batch(self):
        self.current_batch = self.input_buffer.remove_batch()
        
    def process_batch(self):
        if self.current_batch is not None:
            self.current_batch.increment_task()
            if self.current_batch.is_done():
                self.output_buffer.add_batch(self.current_batch)
                self.current_batch = None
                
    def get_processing_time(self):
        if self.current_batch is not None:
            return self.current_batch.get_processing_time()
        else:
            return 0
        
class Unit:
    def __init__(self, unit_number, tasks):
        self.unit_number = unit_number
        self.tasks = tasks
        self.current_task_index = 0
        self.current_batch = None
        
    def is_busy(self):
        return self.current_batch is not None
        
    def next_batch(self):
        task = self.tasks[self.current_task_index]
        if not task.is_busy() and not self.is_busy():
            batch = task.input_buffer.remove_batch()
            if batch is not None:
                self.current_batch = batch
                task.next_batch()
                
    def process_batch(self):
        if self.current_batch is not None:
            self.current_batch.increment_task()
            if self.current_batch.is_done():
                self.current_batch = None
                self.current_task_index += 1
                
    def get_processing_time(self):
        if self.current_batch is not None:
            return self.current_batch.get_processing_time()
        else:
            return 0
        
class ProductionLine:
    def __init__(self, batch_sizes, buffer_capacity):
        self.batches = [Batch(size) for size in batch_sizes]
        self.buffers = [Buffer(buffer_capacity) for _ in range(10)]
        self.tasks = [Task(i+1, self.buffers[i], self.buffers[i+1]) for i in range(9)]
        self.units = [Unit(1, [self.tasks[0], self.tasks[2], self.tasks[5], self.tasks[8]]),
                      Unit(2, [self.tasks[1], self.tasks[4], self.tasks[6]]),
                      Unit(3, [self.tasks[7], self.tasks[8]])]
        self.current_time = 0
        self.scheduler = Scheduler()
        
    def load_batches(self, intervals):
        for i, batch in enumerate(self.batches):
            load_time = intervals[i]
            self.schedule_action(Action(load_time, self.buffers[0].add_batch, batch))
            
    def schedule_action(self, action):
        self.scheduler.add(action)
        
    def run(self):
        while not self.scheduler.is_empty():
            action = self.scheduler.pop()
            self.current_time = action.time
            action.function(*action.args)
            self.schedule_possible_actions()
            
    def schedule_possible_actions(self):
        for buffer in self.buffers:
            if not buffer.is_empty():
                for task in self.tasks:
                    if task.input_buffer == buffer:
                        if not task.is_busy():
                            self.schedule_action(Action(self.current_time + 1, task.next_batch))
        for task in self.tasks:
            if not task.is_busy():
                for unit in self.units:
                    if not unit.is_busy():
                        for task2 in unit.tasks:
                            if task2 == task:
                                self.schedule_action(Action(self.current_time + 1, unit.next_batch))
        for unit in self.units:
            if not unit.is_busy():
                for task in unit.tasks:
                    if not task.is_busy():
                        self.schedule_action(Action(self.current_time + 1, task.next_batch))
        for task in self.tasks:
            if task.is_busy():
                self.schedule_action(Action(self.current_time + task.get_processing_time(), task.process_batch))
        for unit in self.units:
            if unit.is_busy():
                self.schedule_action(Action(self.current_time + unit.get_processing_time(), unit.process_batch))

            
    def optimize_loading_intervals(self):
        pass
    
    def optimize_ordering_heuristic(self):
        pass
    
    def optimize_batch_sizes(self):
        pass

class Action:
    def __init__(self, time, function, *args):
        self.time = time
        self.function = function
        self.args = args
        
class Scheduler:
    def __init__(self):
        self.actions = []
        
    def add(self, action):
        self.actions.append(action)
        self.actions.sort(key=lambda x: x.time)
        
    def pop(self):
        return self.actions.pop(0)
    
    def is_empty(self):
        return len(self.actions) == 0
    

def main():
    batch_sizes = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    buffer_capacity = 10
    loading_intervals = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    production_line = ProductionLine(batch_sizes, buffer_capacity)
    production_line.load_batches(loading_intervals)
    production_line.run()

if __name__ == '__main__':
    main()