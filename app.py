from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pyrebase
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = ""

config={
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "measurementId": ""}



# Connect to MongoDB
client = MongoClient('mongodb+srv://<username>:<pass>@cluster0.ub5pbd6.mongodb.net/?retryWrites=true&w=majority', serverSelectionTimeoutMS=60000)
db = client["Food"]
collection = db["Recipes"]

# Initialize Firebase Admin SDK
firebase=pyrebase.initialize_app(config)
auth = firebase.auth()





@app.route('/notices', methods=['GET', 'POST'])
def notices():
    NoticeBoard = db["Notices"]
    notices = iter(NoticeBoard.find())
    return render_template('noticeBoard.html', notices=notices)

# Home page
@app.route('/')
def index():
    return redirect('/login')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('login'))
        except Exception as e:
            error_message = str(e)
            return render_template('signup.html', error_message=error_message)
    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user_token'] = user['idToken']
            return redirect(url_for('dashboard'))
        except Exception as e:
            error_message = str(e)
            return render_template('login.html', error_message=error_message)
    return render_template('login.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    user_token = session.get('user_token')
    if user_token:
        try:
            # Use the user_token to fetch user-specific data from Firebase Realtime Database
            user_email = auth.get_account_info(user_token)['users'][0]['email']
            return render_template('dashboard.html', user_email=user_email)
        except Exception as e:
            print("Error fetching user data:", e)
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    Poll = db['Poll']
    polls = iter(Poll.find())
    if request.method == 'POST':
        selected_options = {}
        for poll in polls:
            poll_title = poll['title']
            selected_options[poll_title] = request.form.get(poll_title)
            Poll.update_one(
            {"title": poll_title},
            {"$addToSet": {f"{selected_options[poll_title]}": auth.get_account_info(session.get('user_token'))['users'][0]['email']}},
            )
            Poll.update_one({"title":poll_title},{"$push": {"voters": auth.get_account_info(session.get('user_token'))['users'][0]['email']}})      
        return redirect(url_for('dashboard'))
    return render_template('Polls.html',polls=polls)


# Logout
@app.route('/logout')
def logout():
    session.pop('user_token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
