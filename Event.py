# Group 4 - Assignment 3 - Authors: Jon Grendstad, Andreas Blokkum Olborg - TPK4186
class Event:
    def __init__(self, time, action, unit):
        self.time = time
        self.action = action
        self.unit = unit

    def __lt__(self, other_event):
        return self.time < other_event.time

    def __str__(self):
        return "[" + str(self.time) + "|" + str(self.action) + "|" + str(self.unit) + "]"


