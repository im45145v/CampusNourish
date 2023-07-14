from flask import Flask, render_template, redirect, request, session
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# Initialize Firebase Admin SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')  # Replace with your own service account key file
firebase_admin.initialize_app(cred)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.get_user_by_email(email)
            auth.verify_password(password, user.password_hash)

            session['user_id'] = user.uid

            return redirect('/dashboard')
        except auth.AuthError as e:
            error_message = str(e)
            return render_template('login.html', error=error_message)

    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.create_user(
                email=email,
                password=password
            )

            session['user_id'] = user.uid

            return redirect('/dashboard')
        except auth.AuthError as e:
            error_message = str(e)
            return render_template('signup.html', error=error_message)

    return render_template('signup.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    user = auth.get_user(user_id)

    return render_template('dashboard.html', user_email=user.email)

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run()
