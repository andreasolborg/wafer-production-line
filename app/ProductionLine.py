from Task import Task
from Buffer import Buffer
from Unit import Unit
from Batch import Batch
from Scheduler import Scheduler

class ProductionLine:
    '''
    A class that represents the entire production line, with attributes such as a list of units,
    and a scheduler for managing the order of tasks.
    The production line holds a global tick-value to keep track of simultaion time in the production line. 
    This class also assigns batches to tasks, and moves batches between tasks and units. 
    Upon initzialization, the input and output buffers are assigned to tasks in the production line.
    '''
    def __init__(self, units: list[Unit]):
        self.units = units
        self.tick = 0
        # self.scheduler = Scheduler()

    def getUnits(self):
        return self.units
    
    def getTick(self):
        return self.tick
    
    def incrementTick(self):
        for unit in self.getUnits():
            tasks = unit.getTasks()
            for task in tasks:
                task.incrementTick()
        self.tick += 0.1

    def assignInputBufferToTask(self, task: Task, buffer: Buffer):
        task.setInputBuffer(buffer)

    def assignOutputBufferToTask(self, task: Task, buffer: Buffer):
        task.setOutputBuffer(buffer)









def main():
    task1 = Task(1)
    task2 = Task(2)
    task3 = Task(3)
    task4 = Task(4)
    task5 = Task(5)
    task6 = Task(6)
    task7 = Task(7)
    task8 = Task(8)
    task9 = Task(9)
    
    tasksForUnit1 = [task1, task3, task6, task9]
    tasksForUnit2 = [task2, task5, task7]
    tasksForUnit3 = [task4, task8]
    
    unit1 = Unit(tasksForUnit1)
    unit2 = Unit(tasksForUnit2)
    unit3 = Unit(tasksForUnit3)
    

if __name__ == "__main__":
    main()        
    