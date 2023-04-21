class Buffer:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.content = []

    def add_batch(self, batch):
        if self.get_total_wafers() + batch.size <= self.capacity:
            self.content.append(batch)
            return True
        return False

    def remove_batch(self):
        if self.content:
            return self.content.pop(0)
        return None

    def get_total_wafers(self):
        return sum(batch.size for batch in self.content)
    
    def __str__(self):
        return "buffer" + str(self.id)
    
    def content_to_string(self):
        return ", ".join(str(batch) for batch in self.content)
    

