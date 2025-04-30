import os
import csv
import time
from db.connection import connection

#GET DATA FROM TABLE
def get_data():
    mydb = connection()
    cursor = mydb.cursor()
    
    sql = "SELECT * FROM testData"
    
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
        print("Error fetching data: " + str(e))
        
    cursor.close()
    mydb.close()

#FILTER CSV DATA AND SAVE TO NEW CSV
def check_filePath(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                read_csv = csv.DictReader(file)
                needed_data = ['Hours', 'Instructor', 'End_Date', 'Name', 'Days_of_the_Week', 'Start_Date', 'Locations', 'Title']
                new_data = []

                for row in read_csv:
                    if row['Locations'] and row['Locations'] != 'NA':
                        hours_split = [h.strip() for h in row['Hours'].split(';')]
                        days_split = [d.strip() for d in row['Days_of_the_Week'].split(';')] if ';' in row['Days_of_the_Week'] else [row['Days_of_the_Week']] * len(hours_split)
                        locations_split = [l.strip() for l in row['Locations'].split(';')] if ';' in row['Locations'] else [row['Locations']] * len(hours_split)

                        for i in range(len(hours_split)):
                            new_row = {col: row[col] for col in needed_data if col in row}
                            new_row['Hours'] = hours_split[i]
                            new_row['Days_of_the_Week'] = days_split[i] if i < len(days_split) else days_split[0]
                            new_row['Locations'] = locations_split[i] if i < len(locations_split) else locations_split[0]
                            new_data.append(new_row)

                save_to_csv(new_data, 'new_data.csv')
                return new_data

        except Exception as e:
            print("Error reading the file: " + str(e))
    else:
        print("File " + file_path + " does not exist")
        
#SAVE NEW DATA TO ANOTHER CSV      
def save_to_csv(new_data, output_file_path):
    try:
        file_exists = os.path.exists(output_file_path)
        with open(output_file_path, 'w', newline='') as file:
            fieldnames = new_data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(new_data)
        print("Data saved to " + str(output_file_path))
    except Exception as e:
        print("Error saving data to CSV " + str(e))

#WAIT AND INSERT FILE IF IT EXISTS
def wait_insert_file(file_path = "new_data.csv"):
    while not os.path.exists(file_path):
        print("WAITING FOR FILE" + str(file_path))
        time.sleep(10)
    
    print("FOUND FILE" + str(file_path))
    insert_data(file_path)


#INSERT DATA INTO TESTDATA TABLE
def insert_data(file_path='new_data.csv'):
    try:
        if os.path.exists(file_path):
            with open(file_path, mode='r') as file:
                csv_reader = csv.DictReader(file)
                new_data = list(csv_reader)
                
            mydb = connection()
            cursor = mydb.cursor()
            print("ADDING DATA TO testDATA TABLE")
            for row in new_data: 
                
                cursor.execute('''
                    INSERT INTO testData(Hours, Instructor, End_Date, Name, Days_of_the_Week, Start_Date, Locations, Title)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    row['Hours'],
                    row['Instructor'],
                    row['End_Date'],
                    row['Name'],
                    row['Days_of_the_Week'],
                    row['Start_Date'],
                    row['Locations'],
                    row['Title']
                ))
            
            mydb.commit()
            
            #--------------------------- CODE TO SEE THE DATABASE, DELETE IF SUCCESSFUL -----------------------------------
            #cursor.execute('SELECT * FROM testData')
            #rows = cursor.fetchall()
            
            #print("\nContents of testData table after adding data from new_data.csv")
            #for row in rows:
                #print(row)
                
            #------------------------------------- END OF TEST CODE ---------------------------------------------------------
            
            cursor.close()
            mydb.close()
        else:
            print("file does not exist" + str(file_path))
    except Exception as e:
        print("Error inserting data into database: " + str(e))
        
def delete_file(file_path="scheduler_information.csv", new_file_path="new_data.csv"):
    print("=============FILES BEING DELETED IN 20 SECONDS==================")
    time.sleep(20)
        
    if os.path.exists(file_path):
        os.remove(file_path)
        print(file_path + new_file_path + " has been deleted")
    else:
        print(file_path + "does not exist, can not be deleted")
        
    if os.path.exists(new_file_path):
        os.remove(new_file_path)
        print(new_file_path + " has been deleted")
    else:
        print(new_file_path + "does not exist, can not be deleted")
        
    print("CONTENT IN DATABASE")
    mydb = connection()
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM testData')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
        
    cursor.close()
    mydb.close()
    
    
    