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
        self.inputBuffer = None # the input buffer for the task, which is a list of batches
        self.outputBuffer = None
        self.processingTime = self.determineProcessingTime()
        self.validateProcessingTime()
        self.batchInTask = None # the batch that is currently in the task
        self.isProcessing = False # is the task processing a batch? 
        self.isFinished = False # is the task finished processing the batch, so it can be unloaded from the unit?
        self.tick = 0

    def getTaskNumber(self):
        return self.taskNumber

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
    
    def getBatchInTask(self):
        return self.batchInTask
        
    def setBatchInTask(self, batch):
        # check if task is already processing a batch, and if the batch is not None
        if self.getIsProcessing() == True and batch != None:
            raise ValueError("Task is already processing a batch.")
        self.batchInTask = batch
        self.setIsProcessing(True)
        self.setIsFinished(False)

    def setInputBuffer(self, buffer):
        self.inputBuffer = buffer

    def setOutputBuffer(self, buffer):
        self.outputBuffer = buffer

    # if batch has been in task for the processing time, set isFinished to True. Then the batch can be unloaded from the unit, and sent to the next task
    def incrementTick(self, tick: float):
        self.tick += tick
        
        print(f"Task {self.getTaskNumber()} has tick {self.getTick()}.")
        if self.getIsProcessing() == False:
            # check if the task has a batch in it, and if the input buffer has a batch in it
            if self.getBatchInTask() == None and self.inputBuffer != None:
                if self.inputBuffer.getBatches() != None: 
                    self.setBatchInTask(self.inputBuffer.removeBatchFromBuffer())
                    print(f"Batch {self.getBatchInTask()} has been loaded into task {self.getTaskNumber()}.")
            else:
                print(f"Task {self.getTaskNumber()} is not processing a batch.")
        
        if self.getTick() >= self.getProcessingTime():
            print("FINISHED PROCESSING BATCH")
            # check if task has a batch in it, and increment the tick of the batch in the task
            print(f"Task {self.getTaskNumber()} has finished processing batch {self.getBatchInTask()}.")
            if self.getBatchInTask() != None:
                self.getBatchInTask().incrementTick(self.getTick())
            self.setIsFinished(True)
            self.setIsProcessing(False)
            self.tick = 0 # reset the tick to 0 for the next batch that will be processed in the task 

            # send the batch to the output buffer
            if self.outputBuffer != None:
                self.outputBuffer.addBatchToBuffer(self.getBatchInTask())
                print(f"Batch {self.getBatchInTask()} has been sent to the output buffer of task {self.getTaskNumber()}.")
                self.setBatchInTask(None)
            else:
                print(f"Task {self.getTaskNumber()} has no output buffer.")
                

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
        return f"Task {self.getTaskNumber()} has input buffer {self.inputBuffer}, output buffer {self.outputBuffer}, processing time {self.getProcessingTime()}, batch in task {self.getBatchInTask()}, is processing {self.getIsProcessing()}, is finished {self.getIsFinished()}, tick {self.getTick()}."


def main():
    print("This is the Task class.")
    # make 9 tasks and print them

    # for i in range(1, 10):
    #     task = Task(i)
    #     print(task)

    # make a batch of size 20
    batch = Batch(30)

    task1 = Task(1)
    print("Æ")
    buffer1 = Buffer()
    buffer2 = Buffer()
    buffer3 = Buffer()
    task1.setInputBuffer(buffer1)
    task1.setOutputBuffer(buffer2)
    buffer1.addBatchToBuffer(batch)
    print(task1)

    task1.incrementTick(0.5)
    print("Task1 input: ", task1.inputBuffer)
    print("Task1 output: ", task1.outputBuffer)

    print("\n\n********* TASK 2 *********")
    task2 = Task(2)
    task2.setInputBuffer(task1.outputBuffer)
    task2.setOutputBuffer(buffer3)
    print("\n********")
    print("Task 2 input: ", task2.inputBuffer)
    print("Task 2 output: ", task2.outputBuffer)

    print("\n********")
    print(task2)
    task2.incrementTick(3.5)

    print("\n********")
    print("Task 2 input: ", task2.inputBuffer)
    print("Task 2 output: ", task2.outputBuffer)











    # # increment the tick of the task
    # task.incrementTick(3.5)
    # print(task)

      


if __name__ == "__main__":
    main()