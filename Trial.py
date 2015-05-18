import sys # for stdout
import numpy as np

class Trial:
	def __init__(self, trialId):
		self.trialId = trialId
		self.companyNames = []
		self.companyWeights = []
		self.returnsList = []	
		self.trialRisk = -1 
		self.trialReturn = -1
	def setNames(self, names):
		self.companyNames = names	
	def setWeights(self, weights):
		self.companyWeights = weights	
	def setReturnList(self, returnList):
		self.returnList = returnList		
	def calcRiskReturn(self):
		# define matricies	
		meanReturnsMatrix = np.asmatrix(np.mean(self.returnList, axis = 1))
		weightMatrix = np.asmatrix(self.companyWeights)
		rocCovarMatrix = np.asmatrix(np.cov(self.returnList))
		# calculate matricies
		trialRisk = np.sqrt(weightMatrix * rocCovarMatrix * weightMatrix.T)
		trialReturn = weightMatrix * meanReturnsMatrix.T
		# return variables
		self.trialRisk = float(trialRisk)
		self.trialReturn = float(trialReturn)
	def setRisk(self, trialRisk):
		self.trialRisk = trialRisk
	def setReturn(self, trialReturn):
		self.trialReturn = trialReturn
	def printTrial(self):
		for weight in self.companyWeights:
			sys.stdout.write('{0: <20}'.format(str(weight)))
		sys.stdout.write('{0: <20}'.format(str(self.trialRisk)))	
		sys.stdout.write('{0: <20}'.format(str(self.trialReturn)))
		print ("") # for a single new line

