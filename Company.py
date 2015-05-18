#-------------------------------------
# Class called "Company"
# 	Loads data from MySQL for 
#	stock data. 
#-------------------------------------

from CompanyData_databaseHandle import loginCompanyData # for CompanyData database login
import numpy as np # for matricies 
import talib as ta # for technical analysis
import matplotlib.pyplot as plt
from scipy.stats import norm # for normal distribution fit
from datetime import datetime, timedelta 

import sys
import os
import pandas as pa

# conect to database
LOAD_COMPANYDATA_DATABASEHANDLE = loginCompanyData()

def returnValidStartDateIndex(dateList, tryDate):		
	# if the date lands on a weekend, you'll get an error
	# so you need to try the NEXT day and keep on doing so
	# untill you find a day that works	
	if (tryDate in dateList): 
		return dateList.index(tryDate)	
	else: 
		newDate = tryDate + timedelta(days = 1)
		return returnValidStartDateIndex(dateList, newDate)

def returnValidEndDateIndex(dateList, tryDate):
	# if the date lands on a weekend, you'll get an error
	# so you need to try the PREVIOUS day and keep on doing 
	# so untill you find a day that works	
	if (tryDate in dateList):
		return dateList.index(tryDate)
	else: 
		newDate = tryDate - timedelta(days = 1)	
		return returnValidEndDateIndex(dateList, newDate)
	
class Company:
	def __init__(self,ticker):
		self.ticker = ticker
		# loaded data 
		self.loadedDateString = np.array
		self.loadedOpen = np.array
		self.loadedHigh = np.array
		self.loadedLow = np.array	
		self.loadedClose = np.array
		self.loadedVol = np.array	
		self.loadedAdjClose = np.array	
		self.loadedStartDate = datetime
		self.loadedEndDate = datetime
		self.loadedDates = []	
		self.loadedPoints = int	
		# calculated data
		self.mu = 0.0	
		self.stdDev = 0.0
		self.rocAdjClose= np.array
	def loadTicker(self):
		# query database
		query = "SELECT dateString, open, high, low, close, vol, adjClose FROM " + self.ticker + "_priceData"
		numrows = LOAD_COMPANYDATA_DATABASEHANDLE.execute(query)
		resultArray = np.fromiter(LOAD_COMPANYDATA_DATABASEHANDLE.fetchall(), count = numrows, dtype = ('a20, f, f, f, f, i, f'))
		# get columns from result	
		resultDateString = np.array([str(x) for x in resultArray['f0']])
		resultOpen = np.array([float(x) for x in resultArray['f1']])	
		resultHigh = np.array([float(x) for x in resultArray['f2']])	
		resultLow = np.array([float(x) for x in resultArray['f3']])	
		resultClose = np.array([float(x) for x in resultArray['f4']])	
		resultVol = np.array([int(x) for x in resultArray['f5']])	
		resultAdjClose = np.array([float(x) for x in resultArray['f6']])
		# reverse the arrays since they are loaded in backwards (earliet date to latest date)	
		resultDateString = np.fliplr([resultDateString])[0]
		resultOpen = np.fliplr([resultOpen])[0]
		resultHigh = np.fliplr([resultHigh])[0]
		resultLow = np.fliplr([resultLow])[0]
		resultClose = np.fliplr([resultClose])[0]
		resultVol = np.fliplr([resultVol])[0]
		resultAdjClose = np.fliplr([resultAdjClose])[0]
		# load to self objects	
		self.loadedDateString = resultDateString 	
		self.loadedOpen = resultOpen
		self.loadedHigh = resultHigh
		self.loadedLow = resultLow
		self.loadedClose = resultClose
		self.loadedVol = resultVol
		self.loadedAdjClose = resultAdjClose
		# get startDate, endDate, loadedDates and loadedPoints (how many prices)	
		self.loadedStartDate = datetime.strptime(self.loadedDateString[0],"%Y-%m-%d")	
		self.loadedEndDate = datetime.strptime(self.loadedDateString[-1],"%Y-%m-%d")	
		for i in range(len(self.loadedDateString)):
			specificDate = datetime.strptime(self.loadedDateString[i], "%Y-%m-%d")	
			self.loadedDates.append(specificDate)	
		self.loadedPoints = self.loadedAdjClose.shape[0] 
	def calcNorm(self):
		# roc ("rate of change") will produce 10 nas ("not a number")
		self.rocAdjClose = ta.ROC(self.loadedAdjClose)[10:]	
		self.mu, self.stdDev = norm.fit(self.rocAdjClose)
	def getHist(self, group = "rocAdjClose", command = "show"):	
		dataGroup = "" 	
		if (group == "open"):	
			plt.hist(self.loadedOpen, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "open" 	
		elif (group == "high"):
			plt.hist(self.loadedHigh, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "high" 	
		elif (group == "low"):
			plt.hist(self.loadedLow, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "low" 	
		elif (group == "close"):
			plt.hist(self.loadedClose, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "close" 	
		elif (group == "vol"): 
			plt.hist(self.loadedVol, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "vol" 	
		elif (group == "adjClose"): 
			plt.hist(self.loadedAdjClose, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "adjClose" 	
		elif (group == "rocAdjClose"):	
			plt.hist(self.rocAdjClose, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "rocAdjClose" 	
		else: 
			plt.hist(self.rocAdjClose, bins = 89, normed = True, alpha = 0.6)
			dataGroup = "rocAdjClose" 	
		xmin, xmax = plt.xlim()
		x = np.linspace(xmin, xmax, 100)
		p = norm.pdf(x, self.mu, self.stdDev)
		plt.plot(x, p, 'k', linewidth = 2)
		title = self.ticker+": "+dataGroup+"\nmean = %.2f, std = %.2f" % (self.mu, self.stdDev)
		plt.title(title)
		if (command == "save"):
			plt.savefig(self.ticker+"_"+dataGroup+"Histogram.png")
		elif (command == "show"):
			plt.show()	
		else:
			plt.show()	
	def getLineGraph(self, group = "rocAdjClose", command = "show"):
		dataGroup = "" 	
		if (group == "open"):	
			plt.plot(self.loadedOpen)	
			dataGroup = "open" 	
		elif (group == "high"):
			plt.plot(self.loadedHigh)	
			dataGroup = "high" 	
		elif (group == "low"):
			plt.plot(self.loadedLow)	
			dataGroup = "low" 	
		elif (group == "close"):
			plt.plot(self.loadedClose)	
			dataGroup = "close" 	
		elif (group == "vol"): 
			plt.plot(self.loadedVol)	
			dataGroup = "vol" 	
		elif (group == "adjClose"):
			plt.plot(self.loadedAdjClose) 
			dataGroup = "adjClose" 	
		elif (group == "rocAdjClose"):
			plt.plot(self.rocAdjClose)
			dataGroup = "rocAdjClose"
		else: 
			plt.plot(self.rocAdjClose)	
			dataGroup = "rocAdjClose" 	
		title = self.ticker+": "+dataGroup
		plt.title(title)
		if (command == "save"):
			plt.savefig(self.ticker+"_"+dataGroup+"LineGraph.png")
		elif (command == "show"):
			plt.show()	
		else:
			plt.show()	
	def riskReturn_dateRange(self, startDate, endDate):	
		# return the risk and return for the date range
		
		# make sure start date and end date are valid
		# they won't be if they land on a weekend
		startDateIndex = returnValidStartDateIndex(self.loadedDates, startDate)
		endDateIndex = returnValidEndDateIndex(self.loadedDates, endDate) 
		dateRangePrices = self.loadedAdjClose[startDateIndex:endDateIndex]
		
		dateRangeRoc = ta.ROC(dateRangePrices)
		dateRangeRoc = dateRangeRoc[10:]
		dateRangeRisk = np.std(dateRangeRoc)
		dateRangeReturn = dateRangePrices[-1] - dateRangePrices[0]
		return (dateRangeRisk, dateRangeReturn)
	def rocAdjClose_dateRange(self, startDate, endDate):
		startDateIndex = returnValidStartDateIndex(self.loadedDates, startDate)
		endDateIndex = returnValidEndDateIndex(self.loadedDates, endDate) 
		dateRangePrices = self.loadedAdjClose[startDateIndex:endDateIndex]
		
		dateRangeRoc = ta.ROC(dateRangePrices)
		dateRangeRoc = dateRangeRoc[10:]
		return dateRangeRoc
	
#----Test example----
#test = Company("XOM")
#test.loadTicker()
#test.calcNorm()
#test.getHist("rocAdjClose", "save")
#test.getHist("rocAdjClose") 
#test.getLineGraph("adjClose")
#startdate = datetime(test.loadedStartDate.year, test.loadedStartDate.month, test.loadedStartDate.day)
#somedate = datetime(2010,1,1,0,0)
#enddate = test.loadedEndDate
#Risk, Return = test.riskReturn_dateRange(somedate,enddate)
#print (Risk)
#print (Return)
#print(test.loadedDates[0])
#print(test.loadedPoints)
#print(str(test.loadedStartDate.year)+","+str(test.loadedStartDate.month)+","+str(test.loadedStartDate.day))
#print(str(test.loadedEndDate.year)+","+str(test.loadedEndDate.month)+","+str(test.loadedEndDate.day))
