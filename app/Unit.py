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
    def __init__(self, tasks: list):
        self.tasks = tasks
        self.batchInUnit = None # the batch that is currently in the unit
        self.isProcessing = False # is the unit processing a batch? 
        self.tick = 0
            
    def getTasks(self):
        return self.tasks
    
    def getBatchInUnit(self):
        return self.batchInUnit
    
    def unitIsEmpty(self):
        if self.getBatchInUnit() == None:
            return True
        return False
    
    

        
        