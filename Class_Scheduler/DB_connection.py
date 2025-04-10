import mysql.connector
#CONNECTION TO RADY SERVER
mydb = mysql.connector.connect(
    host = "radyweb.wsc.western.edu",
    user = "shargrave",
    password = "we$terncl@sses",
    database = "westernclasses"
)

cursor = mydb.cursor()
#CREATE TABLES
#cursor.execute("CREATE TABLE testData (name VARCHAR(255), address VARCHAR(255))")
sql = "INSERT INTO testData (name, address) VALUES (%s, %s)"
sql1 = "INSERT INTO testData(name, address) VALUES (%s, %s)"
val = ("John", "testAddress")
val1 = ("testName", "NewAddress")
cursor.execute(sql, val)
cursor.execute(sql1, val1)




#SHOWING THE DATABSE AND TABLES IN THE DATABASE
#cursor.execute("SHOW DATABASES")
cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)
    
#PRINTING THE DATA WITHIN THE TABLES
query = "select * from testData"
cursor.execute(query)
rows=cursor.fetchall()
print(rows)


