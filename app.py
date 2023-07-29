from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pyrebase
from pymongo import MongoClient
import var
import jinja2

app = Flask(__name__)
app.secret_key = var.secret_key_var

# config={
#   "apiKey": "",
#   "authDomain": "",
#   "databaseURL": "",
#   "projectId": "",
#   "storageBucket": "",
#   "messagingSenderId": "",
#   "appId": "5",
#   "measurementId": ""}
config=var.config

def unique_count(lst):
    return len(set(lst))

app.jinja_env.filters['unique_count'] = unique_count

# Connect to MongoDB
client = MongoClient(var.mongostr, serverSelectionTimeoutMS=60000)
db = client["Food"]

# Initialize Firebase Admin SDK
firebase=pyrebase.initialize_app(config)
auth = firebase.auth()

admins = ['admin-localID']
admin_mails = ['admin-mail']




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
            if user['localId'] in admins:
                return redirect(url_for('admin'))
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

###############################################################################################

@app.route('/admin')
def admin():
    user_token = session.get('user_token')
    if user_token:
        if auth.get_account_info(user_token)['users'][0]['email'] in admin_mails:
            return render_template('admin.html')


@app.route('/create_poll', methods=['POST'])
def create_poll():
    Polls = db["Poll"]
    option1 = request.form.get('option1')
    option2 = request.form.get('option2')
    new_poll = {
        "title": f"{option1} vs {option2}",
        "options": [option1,option2],
        f"{option1}": [],
        f"{option2}": [],
        "voters": []
    }
    Polls.insert_one(new_poll)
    return redirect('/handle_polls')

@app.route('/remove_polls', methods=['POST'])
def remove_notices():
    Polls = db["Poll"]
    selected_polls = request.form.getlist('remove')
    for title in selected_polls:
        Polls.delete_one({"title": title})
    
    return redirect('/handle_polls')


@app.route('/handle_polls', methods=['GET'])
def handle_polls():
    Polls = db["Poll"]
    polls = list(Polls.find())
    return render_template('ChangePolls.html', polls=polls)


@app.route('/create_notice', methods=['POST'])
def create_notice():
    NoticeBoard = db["Notices"]
    category = request.form.get('category')
    notice = request.form.get('notice')
    NoticeBoard.update_one(
        {"category": category},
        {"$push": {"notices": notice}}
    )
    return redirect('/handle_notices')

@app.route('/remove_notices', methods=['POST'])
def remove_selected_notices():
    NoticeBoard = db["Notices"]
    selected_notices = request.form.getlist('remove')
    for category in NoticeBoard.find():
        for notice in category['notices']:
            if notice in selected_notices:
                NoticeBoard.update_one(
                    {"category": category['category']},
                    {"$pull": {"notices": notice}}
                )
    return redirect('/handle_notices')

@app.route('/handle_notices', methods=['GET'])
def handle_notices():
    NoticeBoard = db["Notices"]
    notices = list(NoticeBoard.find())

    return render_template('ChangeNoticeBoard.html', notices=notices)



@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    if request.method == 'POST':
        ingredients_str = request.form.get('ingredients')
        ingredients = ingredients_str.split(',')

        # Perform the poll logic based on ingredients and display the results
        results = db['Recipes'].find()
        matching_dishes = [document['dish_name'] for document in results if set(ingredients) <= set(document['ingredients'])]
 
        return render_template('ingredients.html', matching_dishes=matching_dishes)
    
    return render_template('ingredients.html')

if __name__ == '__main__':
    app.run(debug=True)

