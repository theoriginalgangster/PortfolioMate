#PortfolioMate

This program is designed to run my own database of securities prices and mostly uses adjusted closing prices. 

Although this project is still a work in progress and does not yet use quadratic constraint optimization, it is, however, still able to create a visibile efficient frontier for back-testing of specified stocks between a certain date range. Although my own database is necessary for this code to work, the SQL associated with the database handle should give enough information to allow you create a sample databse yourself. 

My own data was additionally scraped from EDGAR but is not required for running the backtesting seen in the image bellow. 

![](https://i.imgur.com/9HN20NW.png)
![](http://i.imgur.com/EmSCQgU.png)

**OVERVIEW**

If you're connected to the database...

	shell> python Portfolio.py

If haven't written anything more than the example at the bottom of Portfolio.py, but if you want to include this in a live interperter, you can add any additional companeis if they are in your database. 

*This program makes use of a number of libraries, some of which you may have to compile from C source. Some of them include*

	talib
	pandas
	numpy
	matplotlib
	datetime
	sys

*Quadratic constaint optimization hasn't been implemented yet, but woudl use `cvxopt` which itself uses a GNU optimization library under the hood.* 


This documentation for processing the stock data and fundemental data that is already loaded into MySQL. 

The MySQL database is called "CompanyData" and has two main important features: 
	
	1) Multiple tables for all stocks with columns: 
	
	  	ticker VARCHAR(10),
		dateString VARCHAR(20),
		open FLOAT, 
		high FLOAT, 
		low FLOAT, 
		close FLOAT, 
		vol INT(11),
		adjClose FLOAT	
		 
	   For each day from the companies exsistance. 	
	
	2) A single table for all stocks containing fundemental analysis data called "EDGARFundementalData" with the follong fields: 
		
		Ticker VARCHAR(20), 
		QTF VARCHAR(20), 
		DateQ4 VARCHAR(20), 
		DateQ3 VARCHAR(20), 
		DateQ2 VARCHAR(20), 
		DateQ1 VARCHAR(20), 
		CIlabel VARCHAR(20), 
		Address VARCHAR(20), 
		City VARCHAR(20), 
		PhoneNumber VARCHAR(20), 
		KFRSlabel VARCHAR(20), 
		KFRSYear VARCHAR(20), 
		NetIncOverCommEquity FLOAT, 
		TotalLiabOverTotalAssets FLOAT, 
		NetIncOverTotalAssets FLOAT, 
		TotalLiabOverInvCap FLOAT, 
		PretaxIncOverNetSales FLOAT, 
		InterestCoverageRatio FLOAT, 
		NetIncOverNetSales FLOAT, 
		CurrDebtOverEquity FLOAT, 
		CashFlowOverNetSales FLOAT, 
		LTDOverEquity FLOAT, 
		NetReceivablesTurnover FLOAT, 
		QuickRatio FLOAT, 
		InventoryTurnover FLOAT, 
		CurrentRatio FLOAT, 
		InventoryDaySales FLOAT, 
		NetRecOverCurrAssets FLOAT, 
		NetSalesOverWorkCap FLOAT, 
		InvOverCurrAssets FLOAT, 
		NetSalesOverPPAndE FLOAT, 
		ISlabel VARCHAR(20), 
		TotalRevenuesNetSalesQ4 FLOAT, 
		TotalRevenuesNetSalesQ3 FLOAT, 
		TotalRevenuesNetSalesQ2 FLOAT, 
		TotalRevenuesNetSalesQ1 FLOAT, 
		CostOfGoodsSoldQ4 FLOAT, 
		CostOfGoodsSoldQ3 FLOAT, 
		CostOfGoodsSoldQ2 FLOAT, 
		CostOfGoodsSoldQ1     FLOAT, 
		SellingAndAdminExpsQ4 FLOAT, 
		SellingAndAdminExpsQ3 FLOAT, 
		SellingAndAdminExpsQ2 FLOAT, 
		SellingAndAdminExpsQ1 FLOAT, 
		OperatingIncomeQ4 FLOAT, 
		OperatingIncomeQ3 FLOAT, 
		OperatingIncomeQ2 FLOAT, 
		OperatingIncomeQ1 FLOAT, 
		InterestExpQ4 FLOAT, 
		InterestExpQ3 FLOAT, 
		InterestExpQ2 FLOAT, 
		InterestExpQ1 FLOAT, 
		PretaxIncomeQ4 FLOAT, 
		PretaxIncomeQ3 FLOAT, 
		PretaxIncomeQ2 FLOAT, 
		PretaxIncomeQ1 FLOAT, 
		OtherIncomeQ4 FLOAT, 
		OtherIncomeQ3 FLOAT, 
		OtherIncomeQ2 FLOAT, 
		OtherIncomeQ1 FLOAT, 
		NetIncomeQ4 FLOAT, 
		NetIncomeQ3 FLOAT, 
		NetIncomeQ2 FLOAT, 
		NetIncomeQ1 FLOAT, 
		BSlabel VARCHAR(20), 
		CashAndShortTermInvestmentsQ4 FLOAT, 
		CashAndShortTermInvestmentsQ3 FLOAT, 
		CashAndShortTermInvestmentsQ2 FLOAT, 
		CashAndShortTermInvestmentsQ1 FLOAT, 
		ReceivablesTotalQ4 FLOAT, 
		ReceivablesTotalQ3 FLOAT, 
		ReceivablesTotalQ2 FLOAT, 
		ReceivablesTotalQ1 FLOAT, 
		InventoriesTotalQ4 FLOAT, 
		InventoriesTotalQ3 FLOAT, 
		InventoriesTotalQ2 FLOAT, 
		InventoriesTotalQ1 FLOAT, 
		TotalCurrentAssetsQ4 FLOAT, 
		TotalCurrentAssetsQ3 FLOAT, 
		TotalCurrentAssetsQ2 FLOAT, 
		TotalCurrentAssetsQ1 FLOAT, 
		NetPropertyPlatAndEquipmentQ4 FLOAT, 
		NetPropertyPlatAndEquipmentQ3 FLOAT, 
		NetPropertyPlatAndEquipmentQ2 FLOAT, 
		NetPropertyPlatAndEquipmentQ1 FLOAT, 
		TotalAssetsQ4 FLOAT, 
		TotalAssetsQ3 FLOAT, 
		TotalAssetsQ2 FLOAT, 
		TotalAssetsQ1 FLOAT, 
		AccountsPayableQ4 FLOAT, 
		AccountsPayableQ3 FLOAT, 
		AccountsPayableQ2 FLOAT, 
		AccountsPayableQ1 FLOAT, 
		DebtInCurrentLiabilitiesQ4 FLOAT, 
		DebtInCurrentLiabilitiesQ3 FLOAT, 
		DebtInCurrentLiabilitiesQ2 FLOAT, 
		DebtInCurrentLiabilitiesQ1 FLOAT, 
		TotalCurrentLiabilitiesQ4 FLOAT, 
		TotalCurrentLiabilitiesQ3 FLOAT, 
		TotalCurrentLiabilitiesQ2 FLOAT, 
		TotalCurrentLiabilitiesQ1 FLOAT, 
		LongTermDebtQ4 FLOAT, 
		LongTermDebtQ3 FLOAT, 
		LongTermDebtQ2 FLOAT, 
		LongTermDebtQ1 FLOAT, 
		TotalLiabilitiesQ4 FLOAT, 
		TotalLiabilitiesQ3 FLOAT, 
		TotalLiabilitiesQ2 FLOAT, 
		TotalLiabilitiesQ1 FLOAT, 
		MinorityInterestQ4 FLOAT, 
		MinorityInterestQ3 FLOAT, 
		MinorityInterestQ2 FLOAT, 
		MinorityInterestQ1 FLOAT, 
		PreferredStockQ4 FLOAT, 
		PreferredStockQ3 FLOAT, 
		PreferredStockQ2 FLOAT, 
		PreferredStockQ1 FLOAT, 
		CommonStockQ4 FLOAT, 
		CommonStockQ3 FLOAT, 
		CommonStockQ2 FLOAT, 
		CommonStockQ1 FLOAT, 
		RetainedEarningsQ4 FLOAT, 
		RetainedEarningsQ3 FLOAT, 
		RetainedEarningsQ2 FLOAT, 
		RetainedEarningsQ1 FLOAT, 
		TreasuryStockQ4 FLOAT, 
		TreasuryStockQ3 FLOAT, 
		TreasuryStockQ2 FLOAT, 
		TreasuryStockQ1 FLOAT, 
		TotalStockholdersEquityQ4 FLOAT, 
		TotalStockholdersEquityQ3 FLOAT, 
		TotalStockholdersEquityQ2 FLOAT, 
		TotalStockholdersEquityQ1 FLOAT, 
		TotalLiabilitiesAndStockholdersEquityQ4 FLOAT, 
		TotalLiabilitiesAndStockholdersEquityQ3 FLOAT, 
		TotalLiabilitiesAndStockholdersEquityQ2 FLOAT, 
		TotalLiabilitiesAndStockholdersEquityQ1 FLOAT, 
		CFlabel VARCHAR(20), 
		NetCashProvidedByOperatingActivitiesQ4 FLOAT, 
		NetCashProvidedByOperatingActivitiesQ3 FLOAT, 
		NetCashProvidedByOperatingActivitiesQ2 FLOAT, 
		NetCashProvidedByOperatingActivitiesQ1 FLOAT, 
		NetCashProvidedByInvestingActivitiesQ4 FLOAT, 
		NetCashProvidedByInvestingActivitiesQ3 FLOAT, 
		NetCashProvidedByInvestingActivitiesQ2 FLOAT, 
		NetCashProvidedByInvestingActivitiesQ1 FLOAT, 
		NetCashProvidedByFinancingActivitiesQ4 FLOAT, 
		NetCashProvidedByFinancingActivitiesQ3 FLOAT, 
		NetCashProvidedByFinancingActivitiesQ2 FLOAT, 
		NetCashProvidedByFinancingActivitiesQ1 FLOAT, 
		SOlabel VARCHAR(20), 
		DateQM VARCHAR(20), 
		NoOwners INT, 
		sharesheld INT


