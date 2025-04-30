import mysql.connector
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
#CONNECTION TO RADY SERVER
def connection():
    mydb = mysql.connector.connect(
        host = "radyweb.wsc.western.edu",
        user = "shargrave",
        password = "we$terncl@sses",
        database = "westernclasses"
    )
    return mydb

#Creating the table to store events
def create_event_table():
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    #print("-----DROPPING TABLE events----")
    #cursor.execute("DROP TABLE IF EXISTS events;")
    print("-----CREATING TABLE events-----")
    query = """
    CREATE TABLE IF NOT EXISTS events (
        Name VARCHAR(255),
        EventName VARCHAR(255),
        Email VARCHAR(255),
        StartDate DATE,
        EndDate DATE,
        StartTime TIME,
        EndTime TIME,
        Location VARCHAR(255)
        );  
        """
    
    cursor.execute(query)
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
#Temporary events table
def create_TMPevent_table():
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    #print("-----DROPPING TABLE TMPevents----")
    #cursor.execute("DROP TABLE IF EXISTS TMPevents;")
    print("-----CREATING TABLE TMPevents-----")
    query = """
    CREATE TABLE IF NOT EXISTS TMPevents (
        Name VARCHAR(255),
        EventName VARCHAR(255),
        Email VARCHAR(255),
        StartDate DATE,
        EndDate DATE,
        StartTime TIME,
        EndTime TIME,
        Location VARCHAR(255)
        );  
        """
    
    cursor.execute(query)
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
    
def get_all_tmp_events():
    mydb = connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("USE westernclasses;")
    cursor.execute("SELECT * FROM TMPevents;")
    data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return data

def get_all_events():
    mydb = connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("USE westernclasses;")
    cursor.execute("SELECT * FROM events;")
    newdata = cursor.fetchall()
    cursor.close()
    mydb.close()
    return newdata

#CREATE TEST DATA TABLE
def create_table():
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    print("-----DROPPING TABLE TESTDATA-----")
    cursor.execute("DROP TABLE IF EXISTS testData;")
    print("-----CREATING TABLE testData-----")
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
    #print("-----DROPPING TABLE USERDATA-----")
    #cursor.execute("DROP TABLE IF EXISTS userData;")
    #cursor.execute("DELETE FROM testData;")
    #print("-----CREATING TABLE-----")
    query = """
    CREATE TABLE IF NOT EXISTS userData (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255),
        userType VARCHAR(255)
    );
    """
    
    cursor.execute(query)
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
def get_users(exclude_user):
    mydb = connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("USE westernclasses;")
    cursor.execute("SELECT * FROM  userData WHERE user_id != %s;", (exclude_user,))
    users = cursor.fetchall()
    cursor.close()
    mydb.close()
    return users

def get_user(username):
    mydb = connection()
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("USE westernclasses;")
    cursor.execute("SELECT * FROM  userData WHERE username = %s;", (username,))
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    return user
    

def insert_into_TMPevents(Name,EventName, Email,StartDate,EndDate,StartTime,EndTime,Location):
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    
    query = """
    INSERT INTO TMPevents (Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    cursor.execute(query, (Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location))
    mydb.commit()
    cursor.close()
    mydb.close()


#ADDING USER TO USER TABLE
def insert_user(username, hashed_password, userType):
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    
    query = """
    INSERT INTO userData (username, password, userType)
    VALUES (%s, %s, %s);
    """
    
    cursor.execute(query, (username, hashed_password, userType))
    mydb.commit()
    print(f"user {username} inserted successfully")
    cursor.close()
    mydb.close()
    
def removeUser(username):
    mydb = connection()
    cursor = mydb.cursor()
    
    cursor.execute("USE westernclasses;")
    
    query = "DELETE FROM userData WHERE username = %s LIMIT 1;"
    
    cursor.execute(query, (username,))
    mydb.commit()
    cursor.close()
    mydb.close()
    
def update_user(old_username, new_username=None, new_password=None, new_userType=None):
    mydb = connection()
    cursor = mydb.cursor()

    cursor.execute("USE westernclasses;")

    fields = []
    values = []

    if new_username:
        fields.append("username = %s")
        values.append(new_username)

    if new_password:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        fields.append("password = %s")
        values.append(hashed_password)

    if new_userType:
        fields.append("userType = %s")
        values.append(new_userType)

    if not fields:
        print("Nothing to update.")
        return

    update_query = "UPDATE userData SET " + ", ".join(fields) + " WHERE username = %s"
    values.append(old_username)

    cursor.execute(update_query, tuple(values))
    mydb.commit()
    cursor.close()
    mydb.close()
    
#Insert Data into event table after event has been confirmed
def insert_into_events(Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location):
    mydb = connection()
    cursor = mydb.cursor()
    cursor.execute("USE westernclasses;")
    query = """
        INSERT INTO events (Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    cursor.execute(query, (Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location))
    mydb.commit()
    cursor.close()
    mydb.close()
    
#Remove event from TMPevents if denied
def remove_from_TMPevents(Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location):
    mydb = connection()
    cursor = mydb.cursor()
    cursor.execute("USE westernclasses;")
    query = """
        DELETE FROM TMPevents WHERE
            Name=%s AND EventName=%s AND Email=%s AND StartDate=%s AND EndDate=%s
            AND StartTime=%s AND EndTime=%s AND Location=%s
        LIMIT 1;
    """
    cursor.execute(query, (Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location))
    mydb.commit()
    cursor.close()
    mydb.close()

#Remove event from events table
def remove_from_events(Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location):
    mydb = connection()
    cursor = mydb.cursor()
    cursor.execute("USE westernclasses;")
    query = """
        DELETE FROM events WHERE
            Name=%s AND EventName=%s AND Email=%s AND StartDate=%s AND EndDate=%s
            AND StartTime=%s AND EndTime=%s AND Location=%s
        LIMIT 1;
    """
    cursor.execute(query, (Name, EventName, Email, StartDate, EndDate, StartTime, EndTime, Location))
    mydb.commit()
    cursor.close()
    mydb.close()
    

