from flask import *
from db.handle_data import check_filePath, get_data, insert_data, wait_insert_file, delete_file
from db.connection import removeUser, update_user, get_user, get_users, create_table, insert_user, create_user_table, connection, create_event_table, insert_into_TMPevents, get_all_tmp_events, create_TMPevent_table, insert_into_events, remove_from_TMPevents, get_all_events, remove_from_events 
import json
import pandas as pd
import requests
import os
import time
import copy
from datetime import datetime
from flask_bcrypt import Bcrypt
import difflib

app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.secret_key = "testKeythatislongforsecurity"
bcrypt = Bcrypt(app)

#---------------------------------
#-----------CODE FOR API----------
#---------------------------------

#Calendar data for gym
@app.route('/api/gym')
def calendar_data():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Paul Wright Gymnasium%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    
    
#Calendar data for crawford
@app.route('/api/crawford')
def calendar_data_crawford():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Crawford%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    

#Calendar data for Borick
@app.route('/api/borick')
def calendar_data_borick():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Borick%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    
#Calendar data for Hurst
@app.route('/api/hurst')
def calendar_data_hurst():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Hurst%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500


#Calendar data for Taylor
@app.route('/api/taylor')
def calendar_data_taylor():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Taylor%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    
    
#Calendar data for Rady
@app.route('/api/rady')
def calendar_data_rady():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Rady%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    
    
#Calendar data for Quigley
@app.route('/api/quigley')
def calendar_data_quigley():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Quigley%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    
    
#Calendar data for Kelly
@app.route('/api/kelley')
def calendar_data_kelley():
    try:
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("USE westernclasses;")
        cursor.execute("SELECT * FROM testData WHERE Locations LIKE 'Kelley%'")
        data = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(data)
    except Exception as e:
        print("Error fetching calendar data: ", e)
        return jsonify({'error' : 'Could not getch calendar data'}), 500
    
 
#------------------------------
#----------CODE FOR LOGIN------
#------------------------------
    
    
#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']   
    
        mydb = connection()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM userData WHERE username = %s;", (username,))
        user = cursor.fetchone()
        #cursor.fetchall()
        cursor.close()
        mydb.close()
    
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = username
            return redirect(url_for('loginhome'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

#HOME PAGE AFTER LOGIN
@app.route('/homeLogin')
def loginhome():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user_data = get_user(username)
    
    if not user_data:
        return redirect(url_for('loginhome'))
    
    user_id = user_data['user_id']
    user_type = user_data['userType']
    return render_template('home.html', username=username, user_id=user_id, user_type=user_type)


#Create new user
@app.route('/create', methods=['GET', 'POST'])
def createUser():
    if 'user' not in session:
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        userType = request.form['userType']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        insert_user(username, hashed_password, userType)
        
        return redirect(url_for('loginhome'))
    return render_template('create.html')


#Update User
@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'user' not in session:
        return render_template('login.html')
    users = get_users(exclude_user=1)
    return render_template('update.html', userData=users)

#User can add updated data
@app.route('/updateUser', methods=['GET', 'POST'])
def updateUser():
    if 'user' not in session:
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        return render_template('updateUser.html', username=username)
    return redirect(url_for('update'))

@app.route('/handle_update', methods=['POST'])
def handle_update():
    if 'user' not in session:
        return render_template('login.html')
    
    old_username = request.form.get('old_username')
    new_username = request.form.get('username')
    new_password = request.form.get('password')
    new_userType = request.form.get('userType')
    
    update_user(old_username, new_username, new_password, new_userType)
    return redirect(url_for('update'))

@app.route('/removeUser', methods=['POST'])
def remove_user():
    if 'user' not in session:
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        removeUser(username)
        return redirect(url_for('loginhome'))
    return render_template('update.html')
    
    

#-----------------------------
#----------CODE FOR ROOM REQUEST
#-------------------------------

@app.route('/roomRequest')
def view_requests():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user_data = get_user(username)
    
    if not user_data:
        return redirect(url_for('login'))
    
    user_type = user_data['userType']
    
    all_tmp_events = get_all_tmp_events()
    all_events = get_all_events()
    
    allowed_locations = []
    if user_type == "gym" or user_type == "any":
        allowed_locations.append("gym")
    if user_type == "taylor" or user_type == "any":
        allowed_locations.append("taylor")
    if user_type == "borick" or user_type =="any":
        allowed_locations.append("borick")
    if user_type == "quigley" or user_type == "any":
        allowed_locations.append("quigley")
    if user_type == "hurst" or user_type == "any":
        allowed_locations.append("hurst")
    if user_type == "kelley" or user_type == "any":
        allowed_locations.append("kelley")
    if user_type == "rady" or user_type == "any":
        allowed_locations.append("rady")
    if user_type == "crawford" or user_type == "any":
        allowed_locations.append("crawford")

    def is_allowed(event):
        location = event.get('Location', '').lower()
        return any(loc in location for loc in allowed_locations)

    filtered_tmp_events = [e for e in all_tmp_events if is_allowed(e)]
    filtered_events = [e for e in all_events if is_allowed(e)]
    
    return render_template('roomRequest.html', TMPevents=filtered_tmp_events, events=filtered_events)

#LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('loginhome'))

#CHECKING LOGIN SO USER DOES NOT ACCESS 'HIDDEN' ROUTES
@app.before_request
def check_login():
    protected_routes = ['admin', 'test', 'homeLogin', 'create']
    if 'user' not in session and request.endpoint in protected_routes:
        return redirect(url_for('login'))
    

#--------------------------------
#-------INITIAL HOME PAGE--------
#--------------------------------
    
#HOME
@app.route('/')
def home():
    create_user_table() #CREATE USER TABLE
    #create_table()
    create_TMPevent_table()
    create_event_table()
    
    return render_template("index.html")



#------------------------------------------------------
#------------CODE BELOW IS FOR REQUESTING ROOMS--------
#------------------------------------------------------

#Requst room Gym
@app.route('/requestGym', methods=['GET', 'POST'])
def room_request():
    try:
        response = requests.get('http://localhost:8080/api/gym')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request', methods=['POST'])
def handle_data():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))


#Crawford
@app.route('/requestCrawford', methods=['GET', 'POST'])
def room_request_crawford():
    try:
        response = requests.get('http://localhost:8080/api/crawford')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_crawford.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_crawford.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_crawford.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_crawford.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_crawford', methods=['POST'])
def handle_data_crawford():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))

#Borick
@app.route('/requestBorick', methods=['GET', 'POST'])
def room_request_borick():
    try:
        response = requests.get('http://localhost:8080/api/borick')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_borick.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_borick.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_borick.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_borick.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_borick', methods=['POST'])
def handle_data_borick():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))

#Hurst
@app.route('/requestHurst', methods=['GET', 'POST'])
def room_request_hurst():
    try:
        response = requests.get('http://localhost:8080/api/hurst')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_hurst.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_hurst.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_hurst.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_hurst.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_hurst', methods=['POST'])
def handle_data_hurst():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))

#Taylor
@app.route('/requestTaylor', methods=['GET', 'POST'])
def room_request_taylor():
    try:
        response = requests.get('http://localhost:8080/api/taylor')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_taylor.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_taylor.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_taylor.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_taylor.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_taylor', methods=['POST'])
def handle_data_taylor():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))


#Rady
@app.route('/requestRady', methods=['GET', 'POST'])
def room_request_rady():
    try:
        response = requests.get('http://localhost:8080/api/rady')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_rady.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_rady.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_rady.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_rady.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_rady', methods=['POST'])
def handle_data_rady():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))

#Quigley
@app.route('/requestQuigley', methods=['GET', 'POST'])
def room_request_quigley():
    try:
        response = requests.get('http://localhost:8080/api/quigley')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_quigley.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_quigley.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_quigley.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_quigley.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_quigley', methods=['POST'])
def handle_data_quigley():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))


#Kelly
@app.route('/requestKelly', methods=['GET', 'POST'])
def room_request_kelly():
    try:
        response = requests.get('http://localhost:8080/api/kelley')
        existing_classes = response.json()
    except Exception as e:
        print("Error fetching events: " + str(e))
        existing_classes = []

    all_rooms = set(event["Locations"] for event in existing_classes)

    if request.method == 'POST':
        form_action = request.form.get("formAction", "")
        user_name = request.form['requestName']
        event_name = request.form['eventName']
        user_email = request.form['emailUser']
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        event_location = request.form.get('eventLocation', '')

        try:
            user_start = datetime.strptime(start_time, '%H:%M')
            user_end = datetime.strptime(end_time, '%H:%M')
        except ValueError:
            return render_template("request_kelly.html", possible_rooms=[], error="Invalid time format.", previous=request.form, form_checked=True)

        rooms_taken = set()

        for event in existing_classes:
            try:
                time_str = event['Hours'].split('|')[1].strip()
                event_start_str, event_end_str = [t.strip() for t in time_str.split('-')]
                event_start = datetime.strptime(event_start_str, '%I:%M %p')
                event_end = datetime.strptime(event_end_str, '%I:%M %p')

                if not (user_end <= event_start or user_start >= event_end):
                    rooms_taken.add(event['Locations'])
            except Exception as e:
                print("Error parsing event: " + str(e))

        possible_rooms = sorted(all_rooms - rooms_taken)

        if form_action == 'get_rooms':
            return render_template("request_kelly.html", possible_rooms=possible_rooms, previous=request.form, form_checked=True)

        if form_action == 'submit_event':
            if event_location not in possible_rooms:
                return render_template("request_kelly.html", possible_rooms=possible_rooms, error="The selected room is not available...", previous=request.form, form_checked=True)

            insert_into_TMPevents(user_name, event_name, user_email, start_date, end_date, start_time, end_time, event_location)
            return redirect(url_for('home'))

    return render_template("request_kelly.html", possible_rooms=[], previous={}, form_checked=False)


#Handle Data accept or deny room request
@app.route('/handle_request_kelly', methods=['POST'])
def handle_data_kelly():
    data = request.form
    
    if data['action'] == 'accept':
        insert_into_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])

    if data['action'] == 'deny':
        remove_from_TMPevents(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
      
    if data['action'] == 'remove':
        remove_from_events(data['Name'], data['EventName'], data['Email'], data['StartDate'], data['EndDate'], data['StartTime'], data['EndTime'], data['Location'])
    return redirect(url_for('view_requests'))


#------------------------------------------------------
#------------CODE BELOW IS FOR PAGE DATA----------------
#------------------------------------------------------

#GYM
@app.route('/gym', methods=['GET'])
def gym():
    target = "Paul Wright Gym"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("gym.html", events=filtered_events)

#CRAWFORD
@app.route('/crawford')
def crawford():
    target = "Crawford Hall"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("crawford.html", events=filtered_events)

#BORICK
@app.route('/borick', methods=['GET'])
def borik():
    target = "Borick Business Building"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("borick.html", events=filtered_events)

#HURST
@app.route('/hurst')
def hurst():
    target = "Hurst Hall"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("hurst.html", events=filtered_events)

#TAYLOR
@app.route('/taylor')
def taylor():
    target = "Taylor Hall"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("taylor.html", events=filtered_events)

#RADY
@app.route('/rady')
def rady():
    target = "Rady Building"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("rady.html", events=filtered_events)

#QUIGLY
@app.route('/quigley')
def quigly():
    target = "Quigley Hall"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("quigley.html", events=filtered_events)

#KELLY
@app.route('/kelly')
def kelly():
    target = "Kelley Hall"
    all_events = get_all_events()

    def is_similar(loc):
        return difflib.SequenceMatcher(None, loc.lower(), target.lower()).ratio() > 0.7

    filtered_events = [event for event in all_events if is_similar(event['Location'])]
    
    return render_template("kelly.html", events=filtered_events)



#------------------------------------------------------
#------------CODE BELOW IS FOR WEB SCRAPING------------
#------------------------------------------------------


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
    undergrad_terms = []
    
    undergrad_search_url = 'https://apps.western.edu/cs/undergrad_search'
    undergrad_options_url = 'https://apps.western.edu/cs/undergrad_options'
    
    #GRAD CODE
    grad_search_url = 'https://apps.western.edu/cs/grad_search'
    grad_options_url = 'https://apps.western.edu/cs/grad_options'
    
    response = requests.get(undergrad_options_url).json()
    undergrad_terms = response["Standard_Term"]
    
    if request.method == 'POST':
        userInput = request.form.get('term')

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
        instructor_information = {}
        
        response = requests.get(grad_options_url).json()
        grad_terms = response["Standard_Term"]
        instructors_graduate = response["Instructors"]

        for instructor in instructors:
            try:
                request_data["query"]["filters"][1]["value"] = instructor
                response = requests.post(undergrad_search_url, json=request_data, timeout=5)
                
                instructor_information[instructor] = response.json()
            except:
                print("fail")
                exit()
                
        for instructor in instructors_graduate:
            try:
                grad_request_data = copy.deepcopy(request_data)
                grad_request_data["query"]["filters"][1]["value"] = instructor
                response = requests.post(grad_search_url, json=grad_request_data, timeout=5)
                print(response)
                instructor_information[instructor + "_grad"] = response.json()
            except Exception as e:
                print("fail" + str(e))
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
        output = "Calender has been updated with " + str(userInput) + "." + " Please press (next) and allow 30 seconds to allow data to be inserted."
        
        
        #ADD CODE TO MAKE IT SO THAT THE testData table is created each time this page is accessed
        create_table
    return render_template("admin.html", output=output, userInput=userInput, terms = undergrad_terms) 
app.run(port=8080)