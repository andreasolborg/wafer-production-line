from Buffer import Buffer
from Batch import Batch

class Task:
    '''
    A task has one output buffer. It does not have an input buffer, but it does have a fixed loading time to unload a batch from a unit.
    A task can perform only one batch at a time.
    Each task has a different processing time.
    The last task in the unit has output buffer with unlimited capacity.
    ********************************************************************
    |Task                1    2     3    4    5     6    7    8     9   |
    |------------------------------------------------------------------ |
    |Processing time   0.5   3.5   1.2   3   0.8   0.5   1   1.9   0.3  |
    |------------------------------------------------------------------ |
    ********************************************************************
    '''
    def __init__(self, taskNumber: int):
        self.taskNumber = taskNumber
        self.validateTaskNumber()
        self.inputBuffer = None
        self.outputBuffer = None
        self.generateBuffers() # sets the input and output buffers
        self.processingTime = self.determineProcessingTime()
        self.validateProcessingTime()
        self.batchInTask = None # the batch that is currently in the task
        self.isProcessing = False # is the task processing a batch? 
        self.isFinished = False # is the task finished processing the batch, so it can be unloaded from the unit?
        self.tick = 0

    def getTaskNumber(self):
        return self.taskNumber
    
    def generateBuffers(self):
        # The first buffer in the production line is independent of other buffers. It is not connected to any other buffer.
        # The last buffer in the production line is independent of other buffers. It is not connected to any other buffer.
        # Logic for the links between buffers:
        # if task number is 1, then the input buffer is None
        # if task number is 9, then the output buffer is None
        # if task number is between 1 and 9, then the input buffer is the output buffer of the previous task<
        if self.getTaskNumber() == 1:
            self.inputBuffer = Buffer()
        else:
            self.inputBuffer = Task(self.getTaskNumber() - 1).getOutputBuffer()



        if self.getTaskNumber() == 9:
            self.outputBuffer = Buffer(isLastBuffer=True) 
        else:
            self.outputBuffer = Buffer()



    def validateTaskNumber(self):
        if self.getTaskNumber() < 1 or self.getTaskNumber() > 9:
            raise ValueError("Task number must be between 1 and 9.")
        
    def determineProcessingTime(self):
        processingTimes = {1: 0.5, 2: 3.5, 3: 1.2, 4: 3, 5: 0.8, 6: 0.5, 7: 1, 8: 1.9, 9: 0.3}
        return processingTimes[self.getTaskNumber()]
    
    def validateProcessingTime(self):
        if self.getProcessingTime() < 0.3 or self.getProcessingTime() > 3.5:
            raise ValueError("Processing time must be between 0.3 and 3.5.")
        
    def getProcessingTime(self):
        return self.processingTime
    
    def getOutputBuffer(self):
        return self.outputBuffer
    
    def getBatchInTask(self):
        if self.getIsProcessing() == False:
            return None
        return self.batchInTask
    
    def setBatchInTask(self, batch):
        # check if task is already processing a batch. If it is, place the batch in the input buffer
        if self.getIsProcessing() == True:
            
        
        self.batchInTask = batch
        self.isProcessing = True


    # if batch has been in task for the processing time, set isFinished to True. Then the batch can be unloaded from the unit, and sent to the next task
    def incrementTick(self, tick: float):
        self.tick += tick
        if self.getTick() >= self.getProcessingTime():
            # check if task has a batch in it, and increment the tick of the batch in the task
            if self.getBatchInTask() != None:
                self.getBatchInTask().incrementTick(self.getTick())
            self.setIsFinished(True)
            self.setIsProcessing(False)
            self.tick = 0 # reset the tick to 0 for the next batch that will be processed in the task 


    def getTick(self):
        return self.tick
    
    def getIsProcessing(self):
        return self.isProcessing
    
    def setIsProcessing(self, isProcessing: bool):
        self.isProcessing = isProcessing

    def getIsFinished(self):
        return self.isFinished
    
    def setIsFinished(self, isFinished: bool):
        self.isFinished = isFinished

    def __str__(self):
        return "Task number: " + str(self.getTaskNumber()) + ". Processing time: " + str(self.getProcessingTime()) + ". Tick: " + str(self.getTick())
    

def main():
    print("This is the Task class.")
    # make 9 tasks and print them

    # for i in range(1, 10):
    #     task = Task(i)
    #     print(task)

    # make a batch of size 20
    batch = Batch(20)
    print(batch)

    #load the batch into task 1
    task = Task(1)
    task.setBatchInTask(batch)

      


if __name__ == "__main__":
    main()