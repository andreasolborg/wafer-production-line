from Task import Task
from Buffer import Buffer
from Unit import Unit
from Batch import Batch

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
            unit.incrementTick(0.1)
        self.tick += 0.1
        

    def assignInputBufferToTask(self, task: Task, buffer: Buffer):
        task.setInputBuffer(buffer)

    def assignOutputBufferToTask(self, task: Task, buffer: Buffer):
        task.setOutputBuffer(buffer)









def main():

    ## Initialize tasks
    task1 = Task(1)
    task2 = Task(2)
    task3 = Task(3)
    task4 = Task(4)
    task5 = Task(5)
    task6 = Task(6)
    task7 = Task(7)
    task8 = Task(8)
    task9 = Task(9)

    tasks = [task1, task2, task3, task4, task5, task6, task7, task8, task9]
    
    ## Initialize buffers
    buffer1 = Buffer(1)
    buffer2 = Buffer(2)
    buffer3 = Buffer(3)
    buffer4 = Buffer(4)
    buffer5 = Buffer(5)
    buffer6 = Buffer(6)
    buffer7 = Buffer(7)
    buffer8 = Buffer(8)
    buffer9 = Buffer(9)
    buffer10 = Buffer(10)

    buffers = [buffer1, buffer2, buffer3, buffer4, buffer5, buffer6, buffer7, buffer8, buffer9]


    ## Initialize units
    tasksForUnit1 = [task1, task3, task6, task9]
    tasksForUnit2 = [task2, task5, task7]
    tasksForUnit3 = [task4, task8]
    unit1 = Unit(tasksForUnit1)
    unit2 = Unit(tasksForUnit2)
    unit3 = Unit(tasksForUnit3)


    ## Initialize production line
    units = [unit1, unit2, unit3]
    productionLine = ProductionLine(units)

    ## Assign buffers to tasks in the production line. 
    productionLine.assignInputBufferToTask(task1, buffer1)
    productionLine.assignOutputBufferToTask(task1, buffer2)
    productionLine.assignInputBufferToTask(task2, buffer2)
    productionLine.assignOutputBufferToTask(task2, buffer3)
    productionLine.assignInputBufferToTask(task3, buffer3)
    productionLine.assignOutputBufferToTask(task3, buffer4)
    productionLine.assignInputBufferToTask(task4, buffer4)
    productionLine.assignOutputBufferToTask(task4, buffer5)
    productionLine.assignInputBufferToTask(task5, buffer5)
    productionLine.assignOutputBufferToTask(task5, buffer6)
    productionLine.assignInputBufferToTask(task6, buffer6)
    productionLine.assignOutputBufferToTask(task6, buffer7)
    productionLine.assignInputBufferToTask(task7, buffer7)
    productionLine.assignOutputBufferToTask(task7, buffer8)
    productionLine.assignInputBufferToTask(task8, buffer8)
    productionLine.assignOutputBufferToTask(task8, buffer9)
    productionLine.assignInputBufferToTask(task9, buffer9)
    productionLine.assignOutputBufferToTask(task9, buffer10)


    
    
    ## Create batches
    batch1 = Batch(20)
    batch2 = Batch(21)

    ## Insert batch1 into the production line
    buffer1.addBatchToBuffer(batch1)
    print("Batch 1 is in buffer 1")
    
    ## Simulate the production line
    for i in range(0, 1000):
        productionLine.incrementTick()
        print("Tick: ", productionLine.getTick())
        print("\n\n")

    

if __name__ == "__main__":
    main()        
    