class Unit:
    def __init__(self, id, tasks):
        self.id = id
        # Prioritize the tasks by time per wafer
        self.tasks = sorted(tasks, key=lambda task: task.time_per_wafer, reverse=False)
        self.time_until_finished = 0
        #for i in self.tasks:
        #    print(i.time_per_wafer, end=" ")
        #print()

    #def prior(self):
    #    self.tasks = sorted(self.tasks, key=lambda task: task.inputbuffer.get_total_wafers(), reverse=True)

    def load(self, current_time, production_line, print_simulation):
        # Check if the unit is locked to a ongoing task
        #self.prior()
        if current_time >= self.time_until_finished:
            return self.choose_next_task(current_time, production_line, print_simulation)
        # We return false if we dont find any task with something in the input buffer
        return False

    def unload(self, current_time, print_simulation): 
        # When we unload we find the first task in the unit with a active batch and unload it
        # A unit will never have two tasks with a active batch at the same time, since its illegal
        for task in self.tasks:
            if task.active_batch:
                return task.unload(current_time, print_simulation)

    # This is the method implemented for choosing the next task for now
    def choose_next_task(self, current_time, production_line, print_simulation):
        # We simply take the first task in the unit that has something in the input buffer
        for task in self.tasks:
            if task.inputbuffer.content:
                time_until_finished = task.load(current_time, production_line, print_simulation)
                if time_until_finished:
                    self.time_until_finished = time_until_finished
                    return True
        return False
            
    def __str__(self):
        return "unit" + str(self.id)
