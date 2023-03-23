# Discrete Event Simulator
import sys

class Action:
	def __init__(self, name, completionDate):
		self.name = name
		self.completionDate = completionDate # the time at which the action is completed

	def getName(self):
		return self.name

	def getCompletionDate(self):
		return self.completionDate

	def setCompletionDate(self, date):
		self.completionDate = date

class Scheduler:
	def __init__(self):
		self.actions = []

	def getActions(self):
		return self.actions

	def getNumberOfActions(self):
		return len(self.actions)
	
	def isEmpty(self):
		return len(self.actions)==0

	def insertAction(self, action): # insert in order of completion date (earliest first)
		position = 0
		while position<self.getNumberOfActions():
			scheduledAction = self.actions[position] 							# get the action at the current position
			if action.getCompletionDate()<scheduledAction.getCompletionDate(): 	# if the action to be inserted has a completion date that is earlier than the action at the current position, then
				break
			position += 1 														# otherwise, move to the next position
		self.actions.insert(position, action) 									# insert the action at the position found above

	def popFirstAction(self):
		if self.isEmpty():
			return None
		return self.actions.pop(0)

class Simulator:
	def __init__(self):
		self.scheduler = Scheduler()

	def newAction(self, name, completionDate): # completionDate is the time at which the action is completed
		action = Action(name, completionDate)
		self.scheduler.insertAction(action) # insert the action in the scheduler in order of completion date, such that the first action to complete is at the front of the list
		return action

	def simulationLoop(self, missionTime): # missionTime is the time at which the simulation ends
		while not self.scheduler.isEmpty():
			action = self.scheduler.popFirstAction()
			if action.getCompletionDate()>missionTime:
				break
			self.performAction(action)

	def performAction(self, action):
		sys.stdout.write("{0:s}\t{1:d}\n".format(action.getName(), action.getCompletionDate())) # print the name and completion date of the action
		name = action.getName() + "'" # add a ' to the name so that it is different from the original action
		completionDate = action.getCompletionDate() + 5 # add 5 to the completion date which means that the new action will be completed 5 time units after the original action
		simulator.newAction(name, completionDate) # create a new action with the same name and a new completion date
		
simulator = Simulator()
simulator.newAction("1", 10)
simulator.newAction("2", 20)
simulator.newAction("3", 15)
simulator.simulationLoop(420)
