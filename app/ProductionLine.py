from Task import Task
from Buffer import Buffer
from Unit import Unit

class ProductionLine:
    '''
    A class that represents the entire production line, with attributes such as a list of units,
    and a scheduler for managing the order of tasks.
    '''
    pass
    





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
    