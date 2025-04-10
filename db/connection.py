import mysql.connector

#CONNECTION TO RADY SERVER
def connection():
    mydb = mysql.connector.connect(
        host = "radyweb.wsc.western.edu",
        user = "shargrave",
        password = "we$terncl@sses",
        database = "westernclasses"
    )
    return mydb

#CREATE TEST DATA TABLE
def create_table():
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    print("-----DROPPING TABLE TESTDATA-----")
    cursor.execute("DROP TABLE IF EXISTS testData;")
    #cursor.execute("DELETE FROM testData;")
    print("-----CREATING TABLE-----")
    query = """
    CREATE TABLE IF NOT EXISTS testData (
        Hours VARCHAR(255),
        Instructor VARCHAR(255),
        End_Date VARCHAR(255),
        Name VARCHAR(255),
        Days_Of_the_Week VARCHAR(255),
        Start_Date VARCHAR(255),
        Locations VARCHAR(255),
        Title VARCHAR(255)
    );
    """
    
    cursor.execute(query)
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
    
#CREATING USER TABLE
def create_user_table():
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    print("-----DROPPING TABLE USERDATA-----")
    cursor.execute("DROP TABLE IF EXISTS userData;")
    #cursor.execute("DELETE FROM testData;")
    print("-----CREATING TABLE-----")
    query = """
    CREATE TABLE IF NOT EXISTS userData (
        username VARCHAR(255),
        password VARCHAR(255)
    );
    """
    
    cursor.execute(query)
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
#ADDING USER TO USER TABLE
def insert_user(username, password):
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    
    query = """
    INSERT INTO userData (username, password)
    VALUES (%s, %s);
    """
    
    cursor.execute(query, (username,password))
    mydb.commit()
    print(f"user {username} inserted successfully")
    cursor.close()
    mydb.close()
