from Wafer import Wafer


class Batch:
    '''
    A batch is a collection of wafers that are processed together. It can either be in the input buffer for a task,
    the output buffer for a task, or in a unit.
    To keep track of time as the batches move through the ProductionLine, each batch has a processing time using a tick counter.
    '''
    def __init__(self, size: int): #evnt wafers: list[Wafer]):
        self.size = size
        self.validateBatchSize()
        self.tick = 0 # starts at 1 so we dont need a input buffer for the first task

        # self.task = 0 #task number that the batch is currently in, not needed because we can use the index of the batch in the task's buffer
        # self.wafers = wafers

    def getTick(self):
        return self.tick
    
    def getBatchSize(self):
        return self.size
    
    def validateBatchSize(self): #batch size is between 20 and 50
        if self.getBatchSize() < 20 or self.getBatchSize() > 50:
            raise ValueError("Batch size must be between 20 and 50.")
        
    def getWafers(self):
        return self.wafers
    
    def incrementTick(self, tick: float):
        self.tick += tick

    def __str__(self):
        return "ID: " + str(id(self))


def main():
    print("This is the Batch class.")
    # make a batch of size 20
    batch = Batch(20)
    print(batch)



if __name__ == "__main__":
    main()
