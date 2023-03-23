from Task import Task
from Buffer import Buffer
from Batch import Batch


class Unit:
    '''
    A unit is a collection of tasks. 
    A unit can perform only one task at a time.
    Batches must be unloaded from units as soon as they are processed.
    Unit 1 handles tasks 1,3,6,9. Unit 2 handles tasks 2,5,7. Unit 3 handles tasks 4,8.
    '''
    def __init__(self, unitNumber: int):
        self.unitNumber = unitNumber
        self.validateUnitNumber()
        self.tasks = self.generateTasks()
        self.batchInUnit = None # the batch that is currently in the unit
        self.isProcessing = False # is the unit processing a batch? 
        self.isFinished = False # is the unit finished processing the batch, so it can be unloaded from the unit?
        self.tick = 0

    def getUnitNumber(self):
        return self.unitNumber
    
    def validateUnitNumber(self):
        if self.getUnitNumber() < 1 or self.getUnitNumber() > 3:
            raise ValueError("Unit number must be between 1 and 3.")
        
    def generateTasks(self):
        if self.getUnitNumber() == 1:
            tasks = [Task(1), Task(3), Task(6), Task(9)]
        elif self.getUnitNumber() == 2:
            tasks = [Task(2), Task(5), Task(7)]
        else:
            tasks = [Task(4), Task(8)]
        return tasks

    def getTasks(self):
        return self.tasks
    
    def unitIsEmpty(self):
        if self.getBatchInUnit() == None:
            return True
        return False
    
    def getBatchInUnit(self):
        return self.batchInUnit
    
    def setBatchInUnit(self, batch):
        if self.unitIsEmpty() == False:
            raise ValueError("Batch is already in unit.")
        self.batchInUnit = batch
        self.setIsProcessing(True)
        self.setIsFinished(False)

        
        