from Task import Task
from Buffer import Buffer
from Batch import Batch


class Unit:
    '''
    A unit is a collection of tasks. 
    A unit can perform only one task at a time.
    Batches must be unloaded from units as soon as they are processed.
    Unit 1 handles tasks 1,3,6,9. Unit 2 handles tasks 2,5,7. Unit 3 handles tasks 4,8.
    Unit can only perform one task at a time.
    '''
    def __init__(self, tasks: list[Task]): 
        self.tasks = tasks
        self.batchInUnit = None # the batch that is currently in the unit
        self.isProcessing = self.determineIsProcessing() # is the unit processing a batch?
        self.tick = 0
            
    def getTasks(self):
        return self.tasks
    
    def unitIsEmpty(self):
        if self.getBatchInUnit() == None:
            return True
        return False
    
    def determineIsProcessing(self):
        if self.determineMultipleTasksProcessing():
            raise ValueError("More than one task is processing a batch. Fix this. (Unit: {})".format(id(self)))
        else:
            for task in self.getTasks():
                if task.getIsProcessing() == True:
                    return True
    
    def determineMultipleTasksProcessing(self):
        count = 0
        for task in self.getTasks():
            if task.getIsProcessing() == True:
                count += 1
        if count > 1:
            return True
        return False
    
    def getIsProcessing(self):
        return self.isProcessing
    
    def setIsProcessing(self, isProcessing: bool):
        self.isProcessing = isProcessing
        
    def getBatchInUnit(self):
        return self.batchInUnit
    
    def setBatchInUnit(self, batch: Batch):
        self.batchInUnit = batch
        

        
def main():
    '''
    Try to simulate a batch moving through the system. This is not a complete simulation. Test task1.incrementTick(5) to throw an error.   
    '''
    task1 = Task(1)
    task2 = Task(2)
    task3 = Task(3)
    task4 = Task(4)
    task5 = Task(5)
    task6 = Task(6)
    task7 = Task(7)
    task8 = Task(8)
    task9 = Task(9)
    
    tasksForUnit1 = [task1, task6, task3, task9]
    tasksForUnit2 = [task2, task5, task7]
    tasksForUnit3 = [task4, task8]
    
    unit1 = Unit(tasksForUnit1)
    unit2 = Unit(tasksForUnit2)
    unit3 = Unit(tasksForUnit3)
    
    # Create a batch, and put it in the input buffer of task 1
    batch = Batch(20)
    batch1 = Batch(21)
    
    buffer1 = Buffer()
    buffer2 = Buffer()
    buffer5 = Buffer()
    buffer6 = Buffer()
    
    task1.setInputBuffer(buffer1)
    task1.setOutputBuffer(buffer2)
    
    task6.setInputBuffer(buffer5)
    task6.setOutputBuffer(buffer6)
    
    task1.getInputBuffer().addBatchToBuffer(batch)
    task1.incrementTick(10) # simulate 5 ticks of processing, it is not done yet. Need 10 ticks to complete.
    
    task6.getInputBuffer().addBatchToBuffer(batch1)
    task6.incrementTick(5) # simulate 5 ticks of processing, it is not done yet. Need 10 ticks to complete.
    
    unit1.determineIsProcessing()
    
    
    
    

    

    

if __name__ == "__main__":
    main()        
    
    
        

        
        