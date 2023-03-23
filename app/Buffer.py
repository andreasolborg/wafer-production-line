from Batch import Batch

class Buffer:
    '''
    A buffer is a queue of batches. 
    It has a maximum capacity of 120 wafers. 
    The last buffer has unlimited capacity.
    Data structure for the buffer is a queue, FIFO/FCFS.
    ''' 
    def __init__(self, isLastBuffer: bool = False): # isLastBuffer is False by default
        self.isLastBuffer = isLastBuffer
        self.determineBufferCapacity()
        self.batches = []
        self.waferCount = 0
        self.validateBufferSize()

    def determineBufferCapacity(self):
        if self.isLastBuffer:
            self.capacity = float("inf") #infinite capacity
        else:
            self.capacity = 120

    def getBufferCapacity(self):
        return self.capacity
    
    def getBatches(self):
        return self.batches
    
    def getBufferSize(self):
        self.waferCount = 0
        for batch in self.batches:
            self.waferCount += batch.getBatchSize()
        return self.waferCount
    
    def validateBufferSize(self):
        if self.isLastBuffer:
            return
        else:
            if self.getBufferSize() > self.getBufferCapacity() or self.getBufferSize() < 0:
                raise ValueError("Buffer size is {}, cannot exceed buffer capacity of {} wafers, or be negative".format(self.getBufferSize(), self.getBufferCapacity()))        
    
    def addBatchToBuffer(self, batch: Batch): #adds a batch to the end of the queue
        self.validateBufferSize()
        batch.incrementTick(1) #it takes 1 tick to add a batch to the buffer
        self.batches.append(batch)

    def removeBatchFromBuffer(self, batch: Batch): #removes a batch from the front of the queue
        self.validateBufferSize()
        batch.incrementTick(1) #it takes 1 tick to remove a batch from the buffer
        return self.batches.pop(0) 
    
    def __str__(self):
        return "Buffer size: " + str(self.getBufferSize()) + " batches. Buffer capacity: " + str(self.getBufferCapacity()) + " wafers."
    

def main():
    print("This is the Buffer class.")
    # make a buffer
    buffer = Buffer()
    print(buffer)
    # make a batch with 20 wafers
    batch1 = Batch(20)
    batch2 = Batch(40)
    batch3 = Batch(40)
    batch4 = Batch(20)
    batch5 = Batch(50)

    listOfBatches = [batch1, batch2, batch3, batch4, batch5]

    # add the batch to the buffer
    buffer.addBatchToBuffer(batch1)
    buffer.addBatchToBuffer(batch2)
    buffer.addBatchToBuffer(batch3)
    buffer.addBatchToBuffer(batch4)
    # print the buffer
    print(buffer)
    # remove the batch from the buffer
    buffer.removeBatchFromBuffer(batch1)
    # print the buffer
    print(buffer)

    for batch in buffer.getBatches():
        print(batch.getTick())

    print(batch1.getTick())

    # make a last buffer with infinite capacity and add batches to it
    lastBuffer = Buffer(True)
    for batch in listOfBatches:
        lastBuffer.addBatchToBuffer(batch)

    print(lastBuffer)



if __name__ == "__main__":
    main()


