class Unit:
    def __init__(self, id, tasks):
        self.id = id
        self.tasks = sorted(tasks, key=lambda obj: obj.time_per_wafer, reverse=True)
        self.time_until_finished = 0

    def load(self, current_time, production_line):
        # Check if the unit is locked to a ongoing task
        if current_time >= self.time_until_finished:
            return self.choose_next_task(current_time, production_line)
        # We return false if we dont find any task with something in the input buffer
        return False

    def unload(self, current_time): 
        # When we unload we find the first task in the unit with a active batch and unload it
        # A unit will never have two tasks with a active batch at the same time, since its illegal
        for task in self.tasks:
            if task.active_batch:
                task.unload(current_time)

    # This is the method implemented for choosing the next task for now
    def choose_next_task(self, current_time, production_line):
        # We simply take the first task in the unit that has something in the input buffer
        for task in self.tasks:
            if task.inputbuffer.content:
                time_until_finished = task.load(current_time, production_line)
                if time_until_finished:
                    self.time_until_finished = time_until_finished
                    return True

    # TODO vhange name to get all tasks with inputbuffer content
    #def get_potential_tasks(self):
    #    potential_tasks = []
    #    for task in self.tasks:
    #        if task.inputbuffer.content:
    #            potential_tasks.append(task)
    #    return potential_tasks

    #def choose_best_task(self, potential_tasks, current_time, production_line):
    #    if potential_tasks:
    #        if len(potential_tasks) == 1:
    #            time_until_finished = potential_tasks[0].load(current_time, production_line)
    #            if time_until_finished:
    #                self.time_until_finished = time_until_finished
    #                return True
    #        else:
    #            for task in potential_tasks:
    #                if task.check_if_outputbuffer_has_space(current_time, production_line):
    #                    time_until_finished = task.load(current_time, production_line)
    #                    if time_until_finished:
    #                        self.time_until_finished = time_until_finished
    #                        return True
            

    def __str__(self):
        return "unit" + str(self.id)
