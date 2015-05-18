import MySQLdb as sql

def loginCompanyData():
	connection = sql.connect("hostname","username","password","databasename")
	CompanyDataHandle = connection.cursor()
	return CompanyDataHandle
