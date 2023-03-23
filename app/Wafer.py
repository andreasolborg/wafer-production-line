class Wafer:
    '''
    Wafer class. It has size of 300mm, and thickness of 0.7mm. 
    This class may be removed in the future as these attributes does not impact the simulation, nor the results.
    '''
    def __init__(self):
        self.size = 300
        self.thickness = 0.7
    
    def getWaferNumber(self):
        return self.waferNumber
    
    def getSize(self):
        return self.size
    
    def getThickness(self):
        return self.thickness
    
    def __str__(self):
        return "Wafer is " + str(self.size) + "mm in size and " + str(self.thickness) + "mm in thickness."


def main():
    print("This is the Wafer class.")
    wafer = Wafer()
    print(wafer)

if __name__ == "__main__":
    main()