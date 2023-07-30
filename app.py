from hedera import AccountCreateTransaction, PrivateKey, Client, AccountId, Hbar, TransferTransaction,AccountBalanceQuery
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pyrebase
from pymongo import MongoClient
import jinja2
import env

app = Flask(__name__)
app.secret_key = "1324456789"

config = env.config

def unique_count(lst):
    return len(set(lst))

app.jinja_env.filters['unique_count'] = unique_count

# Connect to MongoDB
client = MongoClient(env.mongo, serverSelectionTimeoutMS=60000)
db = client["Food"]

# Initialize Firebase Admin SDK
firebase=pyrebase.initialize_app(config)
auth = firebase.auth()

admins = env.admins
admin_mails = env.admin_mails

db = firebase.database()

# Initialize the Hedera client with your account credentials
# Replace with your Hedera network configuration (e.g., mainnet or testnet)
hedera_client = Client("testnet.hedera.com:50211", operator_account_id=env.OPERATOR_ID, operator_private_key=env.OPERATOR_KEY)

def find_or_create_hedera_account(email):
    # Check if the user already has a Hedera account associated with their email
    user_ref = db.collection('users').where('email', '==', email).get()
    for user in user_ref:
        if 'hedera_account_id' in user.to_dict():
            return user.to_dict()['hedera_account_id']

    # If the email doesn't exist in your database, create a new Hedera account for the user
    new_key = PrivateKey.generate()
    resp = AccountCreateTransaction().setKey(new_key.getPublicKey()).setInitialBalance(Hbar(1)).execute(hedera_client)
    account_id = resp.getReceipt(hedera_client).accountId

    # Store the new Hedera account ID in your database associated with the user's email
    user_data = {'email': email, 'hedera_account_id': account_id.toString()}
    db.collection('users').add(user_data)

    return account_id.toString()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Step 1: Create user in Firebase Auth
            user = auth.create_user_with_email_and_password(email, password)

            # Step 2: Create Hedera account and associate it with the user's email
            hedera_account_id = find_or_create_hedera_account(email)

            # For demonstration purposes, we'll store only the Hedera account ID in the user's Firebase data.
            # You may need to extend your database schema to store other user-related data.
            user_data = {'email': email, 'hedera_account_id': hedera_account_id}
            db.collection('users').add(user_data)

            return redirect(url_for('login'))
        except Exception as e:
            error_message = str(e)
            return render_template('signup.html', error_message=error_message)

    return render_template('signup.html')



@app.route('/notices', methods=['GET', 'POST'])
def notices():
    NoticeBoard = db["Notices"]
    notices = iter(NoticeBoard.find())
    return render_template('noticeBoard.html', notices=notices)

# Home page
@app.route('/')
def index():
    return redirect('/login')

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
    polls = list(Poll.find())  # Convert polls to a list instead of an iterator
    if request.method == 'POST':
        selected_options = {}
        for poll in polls:
            poll_title = poll['title']
            selected_options[poll_title] = request.form.get(poll_title)
            Poll.update_one(
                {"title": poll_title},
                {"$addToSet": {f"{selected_options[poll_title]}": auth.get_account_info(session.get('user_token'))['users'][0]['email']}},
            )
            Poll.update_one({"title": poll_title}, {"$push": {"voters": auth.get_account_info(session.get('user_token'))['users'][0]['email']}})
        return redirect(url_for('vote'))
    return render_template('Polls.html', polls=polls)


# Logout
@app.route('/logout')
def logout():
    session.pop('user_token', None)
    return redirect(url_for('index'))



@app.route('/wallet')
def wallet():
    user_token = session.get('user_token')
    if user_token:
        try:
            # Fetch user-specific data from Firebase Realtime Database
            user_email = auth.get_account_info(user_token)['users'][0]['email']
            user_doc = db.collection('users').document(user_email).get().to_dict()
            hedera_account_id = user_doc.get('hedera_account_id')

            if not hedera_account_id:
                # If Hedera account ID is not associated with the user, create one
                hedera_account_id = find_or_create_hedera_account(user_email)
                # Save the Hedera account ID in the user's database document
                db.collection('users').document(user_email).update({'hedera_account_id': hedera_account_id})

            # Get the account balance from Hedera
            balance = AccountBalanceQuery().setAccountId(hedera_account_id).execute(hedera_client).hbars.toString()

            # Get the admin details from the database (replace 'admin_email' with the field name in your database)
            admin_doc = db.collection('admins').document('admin_id').get().to_dict()
            admin_account_id = admin_doc.get('hedera_account_id')

            # Fetch transaction history from the database (replace 'transaction_history' with the field name in your database)
            transaction_history = db.collection('users').document(user_email).get().to_dict().get('transaction_history', [])

            return render_template('wallet.html', user_email=user_email, balance=balance,
                                   admin_account_id=admin_account_id, transaction_history=transaction_history)
        except Exception as e:
            print("Error fetching user data:", e)
            return redirect(url_for('login'))

    return redirect(url_for('login'))


@app.route('/transaction', methods=['POST'])
def transaction():
    user_token = session.get('user_token')
    if user_token:
        try:
            user_email = auth.get_account_info(user_token)['users'][0]['email']
            user_doc = db.collection('users').document(user_email).get().to_dict()
            hedera_account_id = user_doc.get('hedera_account_id')

            if not hedera_account_id:
                return "Hedera account not found. Please create an account first."

            recipient_account_id = request.form.get('recipient')
            amount = float(request.form.get('amount'))

            # Perform the transaction on Hedera network
            # Add your logic here to validate the transaction, check user's balance, etc.
            resp = TransferTransaction().addHbarTransfer(hedera_account_id, Hbar.fromFloat(amount).negated()) \
                .addHbarTransfer(recipient_account_id, Hbar.fromFloat(amount)).execute(hedera_client)

            # Save the transaction details in the user's database document
            db.collection('users').document(user_email).update({
                'transaction_history': {
                    'sender': hedera_account_id,
                    'recipient': recipient_account_id,
                    'amount': amount
                }
            })

            return redirect(url_for('wallet'))
        except Exception as e:
            print("Error processing transaction:", e)
            return "Error processing transaction."

    return redirect(url_for('login'))


@app.route('/pay_admin', methods=['POST'])
def pay_admin():
    user_token = session.get('user_token')
    if user_token:
        try:
            user_email = auth.get_account_info(user_token)['users'][0]['email']
            user_doc = db.collection('users').document(user_email).get().to_dict()
            hedera_account_id = user_doc.get('hedera_account_id')

            if not hedera_account_id:
                return "Hedera account not found. Please create an account first."

            admin_account_id = request.form.get('admin_account_id')
            amount_to_pay = float(request.form.get('amount_to_pay'))

            # Perform the payment transaction to the admin
            # Add your logic here to validate the transaction, check user's balance, etc.
            resp = TransferTransaction().addHbarTransfer(hedera_account_id, Hbar.fromFloat(amount_to_pay).negated()) \
                .addHbarTransfer(admin_account_id, Hbar.fromFloat(amount_to_pay)).execute(hedera_client)

            # Save the transaction details in the user's database document
            db.collection('users').document(user_email).update({
                'transaction_history': {
                    'sender': hedera_account_id,
                    'recipient': admin_account_id,
                    'amount': amount_to_pay
                }
            })

            return redirect(url_for('wallet'))
        except Exception as e:
            print("Error processing payment:", e)
            return "Error processing payment."

    return redirect(url_for('login'))

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

