class Unit:
    def __init__(self, id, tasks):
        self.id = id
        self.tasks = tasks
        self.time_until_finished = 0

    def load(self, current_tick, production_line):
        # Check if the unit is locked to a ongoing task
        if current_tick >= self.time_until_finished:
            return self.choose_next_task(current_tick, production_line)
        # We return false if we dont find any task with something in the input buffer
        return False

    def unload(self, current_tick): 
        # When we unload we find the first task in the unit with a active batch and unload it
        # A unit will never have two tasks with a active batch at the same time, since its illegal
        for task in self.tasks:
            if task.active_batch:
                task.unload(current_tick)

    # This is the method implemented for choosing the next task for now
    def choose_next_task(self, current_tick, production_line):
        # We simply take the first task in the unit that has something in the input buffer
        for task in self.tasks:
            if task.inputbuffer.content:
                time_until_finished = task.load(current_tick, production_line)
                if time_until_finished:
                    self.time_until_finished = time_until_finished
                    return True

    def __str__(self):
        return "unit" + str(self.id)
