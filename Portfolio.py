from Company import Company
import sys # for stdout
import matplotlib.pyplot as plt
from Trial import Trial
from datetime import datetime
import numpy as np

def returnNormalWeights(numberOfWeights):
	weights = []	
	totalWeight = 0	
	# set random weights	
	for weightIndex in range(numberOfWeights):
		randomWeight = np.random.random()
		weights.append(randomWeight)
		totalWeight = totalWeight + randomWeight
	# normalize weights	
	for i in range(len(weights)):
		weights[i] = float(weights[i])/float(totalWeight)	
	return weights	

class Portfolio:
	def __init__(self,portfolioName):
		self.portfolioName = portfolioName
		self.companies = []
		self.minDate = datetime	
		self.maxDate = datetime	
	def loadCompany(self, companyName):
		newCompany = Company(companyName)
		newCompany.loadTicker()
		self.companies.append(newCompany)	
		# reset minDate 
		# minDate is the latest start date of all companies in portfolio
		startDates = []
		for company in self.companies:
			startDates.append(company.loadedStartDate) 
		self.minDate = max(startDates)
		# reset maxDate
		# maxdate is the earliest end date of all companies in portfolio
		endDates = []
		for company in self.companies:
			endDates.append(company.loadedEndDate)
		self.maxDate = min(endDates)	
	def calcNorm(self):
		for company in self.companies:
			company.calcNorm()	
	def printOverview(self):
		print("\nCompany Overview:")	
		# print "ticker:  mu  stdDev  startDate  endDate"	
		print('{0: <10}'.format("ticker:")+'{0: <10}'.format("mu")+'{0: <10}'.format("stdDev")+'{0: <10}'.format("startDate")+'{0: <10}'.format("endDate"))	
		for company in self.companies:
			print ('{0: <10}'.format(str(company.ticker+":"))+'{0: <10}'.format("%.2f"%company.mu)+'{0: <10}'.format("%.2f"%company.stdDev)+'{0: <10}'.format(str(company.loadedStartDate.year))+'{0: <10}'.format(str(company.loadedEndDate.year)))	
		print("minDate: "+str(self.minDate)) 	
	def returnMinDateRandomTrial(self, trialId):
		# create trial object
		trial = Trial(trialId)	
		# create trial variables	
		trialWeights = returnNormalWeights(len(self.companies))
		trialNames = []
		for company in self.companies:
			trialNames.append(company.ticker)	
		trialReturnList = []
		for company in self.companies:
			trialReturnList.append(company.rocAdjClose_dateRange(self.minDate, self.maxDate))
		# assign trial variables to object	
		trial.setWeights(trialWeights)	
		trial.setNames(trialNames)	
		trial.setReturnList(trialReturnList)
		trial.calcRiskReturn()	
		return trial	
	def generateMinDatePointTrial(self, points): 
		# creates points randomized portoflio wights and returns them. 
		# i.e., if points == 100, there will be 100 trails for portfolios,
		# all with different weights and the total risk and return. 
		
		# print lables
		for company in self.companies:	
			sys.stdout.write('{0: <20}'.format(company.ticker))
		sys.stdout.write('{0: <20}'.format("risk"))
		sys.stdout.write('{0: <20}'.format("return"))
		print("") # for new line	
		# get portfolio trials	
		portfolioRisks = []
		portfolioReturns = []	
		for trialIndex in range(points):
			trial = self.testReturnMinDateRandomTrial(trialIndex)	
			#trial.printTrial()	
			portfolioRisks.append(trial.trialRisk)
			portfolioReturns.append(trial.trialReturn)	
		# generate a plot
		# plot trial porfolios	
		plt.plot(portfolioRisks, portfolioReturns, "rx", markersize = 3)
		plt.show()
#	def generateOptimization(self, itterations): 

# Test exmaple
port = Portfolio("testPortfolio")
'''port.loadCompany("FB")
port.loadCompany("GE")
port.loadCompany("GM")
port.loadCompany("XOM")
port.loadCompany("Z")'''
port.loadCompany("AAPL")
port.loadCompany("AMZN")
port.loadCompany("MSFT")
port.loadCompany("BIDU")
port.loadCompany("YHOO")
port.loadCompany("EBAY")
port.calcNorm()
port.printOverview()
port.generateMinDatePointTrial(5000)
'''
fb = Company("FB")
fb.loadTicker()
fb.calcNorm()
fb.getImage("adjClose")	
'''
