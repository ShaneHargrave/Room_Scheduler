from flask import *
from db.handle_data import check_filePath, get_data, insert_data, wait_insert_file, delete_file
from db.connection import create_table, insert_user, create_user_table, connection
import json
import pandas as pd
import requests
import os
import time

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key = "testKey"

#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        mydb = connection()
        cursor = mydb.cursor()
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM userData WHERE username = %s AND password = %s;", (username, password))
    
        user = cursor.fetchone()
        cursor.close()
        mydb.close()
    
        if user:
            session['user'] = username
            return redirect(url_for('loginhome'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

#HOME PAGE AFTER LOGIN
@app.route('/home')
def loginhome():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['user'])

#LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('loginhome'))

#CHECKING LOGIN SO USER DOES NOT ACCESS 'HIDDEN' ROUTES
@app.before_request
def check_login():
    protected_routes = ['admin', 'test']
    if 'user' not in session and request.endpoint in protected_routes:
        return redirect(url_for('login'))
    



#HOME
@app.route('/')
def home():
    create_user_table()
    insert_user('firstUser', 'password')
    return render_template("index.html")

#GYM
@app.route('/gym')
def gym():
    return render_template("gym.html")


#CRAWFORD
@app.route('/crawford')
def crawford():
    return render_template("crawford.html")

#BORICK
@app.route('/borick')
def borik():
    return render_template("borick.html")

#HURST
@app.route('/hurst')
def hurst():
    return render_template("hurst.html")

#TAYLOR
@app.route('/taylor')
def taylor():
    return render_template("taylor.html")

#RADY
@app.route('/rady')
def rady():
    return render_template("rady.html")

#QUIGLY
@app.route('/quigley')
def quigly():
    return render_template("quigley.html")

#KELLY
@app.route('/kelly')
def kelly():
    return render_template("kelly.html")

#TEST DATA ROUTE
@app.route('/test')
def test():
    file_path = "schedule_information.csv"
    file_content = check_filePath(file_path)
    
    try:
        create_table()
        get_data()
        wait_insert_file(file_path = "new_data.csv")
        delete_file(file_path="schedule_information.csv", new_file_path="new_data.csv")
        
    except Exception as e:
        print("Error inserting data: " + str(e))
    return render_template("test.html", file_content=file_content, new_data=file_content)


#SCRAPING CODE
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    output = ""
    userInput = ""
    if request.method == 'POST':
        userInput = request.form.get('userInput')

        undergrad_search_url = 'https://apps.western.edu/cs/undergrad_search'
        undergrad_options_url = 'https://apps.western.edu/cs/undergrad_options'
        
        #GRAD CODE
        #grad_search_url = 'https://apps.western.edu/cs/grad_search'
        #grad_options_url = 'https://apps.western.edu/cs/grad_options'

        columns = ["Hours", "Instructor", "Instructional_Format", "End_Date", "Delivery_Mode", "Name", "Section_Details",
                   "Days_of_the_Week", "Start_Date", "Course", "Locations", "Title", "Not_Online"]

        request_data = {
          "query": {
            "filters": [
              {
                "field": "Standard_Term",
                "value": userInput,
                "include": "True"
              },
              {
                "field": "Instructors",
                "value": "",
                "include": "True"
              }
            ],
            "searches": [
              {
                "field": "Course",
                "value": ""
              },
              {
                "field": "Prerequisite",
                "value": ""
              },
              {
                "field": "Course_Tags",
                "value": ""
              },
              {
                "field": "Subject",
                "value": ""
              },
              {
                "field": "Instructors",
                "value": ""
              },
              {
                "field": "Name",
                "value": ""
              }
            ]
          }
        }

        response = requests.get(undergrad_options_url).json()
        instructors = response["Instructors"]
        #terms = response["Standard_Term"]
        instructor_information = {}

        for instructor in instructors:
            try:
                request_data["query"]["filters"][1]["value"] = instructor
                response = requests.post(undergrad_search_url, json=request_data, timeout=5)
                instructor_information[instructor] = response.json()
            except:
                print("fail")
                exit()

        rows = []

        for instructor, information in instructor_information.items():
            info = json.dumps(information, indent=2)

            for course in information:
                row = []

                for column in columns:
                    if column in course.keys():
                        row.append(course[column])
                    else:
                        row.append("NA")
                rows.append(row)

        def check_for_labs(row):
            hours = row.Hours
            if "; " in hours:
                lab_hours, class_hours = hours.split("; ")
                row.Hours = class_hours
                new_row = row
                new_row.Hours = lab_hours
                pd.concat([df, new_row])

        df = pd.DataFrame(rows, columns=columns)
        df = df.dropna(subset=["Hours"])

        file_path = "schedule_information.csv"
        if not os.path.exists(file_path):
            print("The file " + file_path + " does not exist. Creating the file now.")

        df.to_csv(file_path, index=False)
        print("Data saved to " + file_path)
        output = "Data saved to " + file_path

    return render_template("admin.html", output=output, userInput=userInput)
app.run(port=8080)