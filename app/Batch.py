class Batch:
    def __init__(self, size, id):
        self.id = id
        self.size = size

    def __str__(self):
        return "batch" + str(self.id) + " size: " + str(self.size)