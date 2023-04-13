class Event:
    def __init__(self, time, action, unit):
        self.time = time
        self.action = action
        self.unit = unit

    def __lt__(self, other_event):
        return self.time < other_event.time

    def __str__(self):
        return "[" + str(self.time) + "|" + str(self.action) + "|" + str(self.unit) + "]"

def print_event_queue(event_queue):
    for event in event_queue:
        print(event, end=" ")
    print()
