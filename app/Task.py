import math
import copy
class Task:
    def __init__(self, id, time_per_wafer, inputbuffer, outputbuffer):
        self.id = id
        self.time_per_wafer = time_per_wafer
        self.inputbuffer = inputbuffer
        self.outputbuffer = outputbuffer

        self.active_batch = None

    def load(self, current_time, production_line, print_simulation):
        # A batch must be unloaded immidiatly after its processed so we must ensure its room in the outputbuffer when we unload it
        if self.active_batch:
            return False
        
        if not self.check_if_outputbuffer_has_space(current_time, production_line):
            return False

        self.active_batch = self.inputbuffer.remove_batch()
        
        if self.active_batch: 
            time_until_finished = math.ceil((self.active_batch.size * self.time_per_wafer + current_time) * 10) / 10
            if print_simulation:
                print("tick:", current_time, "---", self, self.active_batch, "loaded and finishes at", time_until_finished)
            return time_until_finished
        
        return False  

    def unload(self, current_time, print_simulation):
        if self.active_batch:
            if self.outputbuffer.add_batch(self.active_batch):
                active_batch_copy = copy.copy(self.active_batch)
                self.active_batch = None
                
                if print_simulation:
                    print("tick:", current_time, "---", self, active_batch_copy, "unloaded")
                    
                if self.outputbuffer.capacity == math.inf:
                    return current_time, active_batch_copy.size

        
    def check_if_outputbuffer_has_space(self, current_time, production_line):
        # If the outputbuffer has infinite capacity it means it is the end buffer and we return True
        if self.outputbuffer.capacity == math.inf:
            return True
        
        # If the outputbuffer has no content we will always have space so we return True
        if not self.outputbuffer.content:
            return True
        
        potential_active_batch = self.inputbuffer.content[0]

        if self.outputbuffer.get_total_wafers() + potential_active_batch.size <= self.outputbuffer.capacity:
            return True 
        
        return False

    def __str__(self):
        return "task" + str(self.id)
