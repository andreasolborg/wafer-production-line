class Batch:
    def __init__(self, id, size):
        self.id = id
        self.size = size

    def __str__(self):
        return "batch" + str(self.id)