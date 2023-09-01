from flask import Flask, render_template,request,session, make_response, redirect,url_for
import json
import bcrypt #used to hash the password

# app = Flask(__name__)
app = Flask(__name__, static_folder="static")
app.secret_key = 'your_secret_key'


# Read existing users from JSON file
def read_users_from_file():
    try:
        with open('users.json', 'r') as file:
            users_data = json.load(file)
            return users_data
    except FileNotFoundError:
        return []

# Write new users to JSON file
def write_users_to_file(users_data):
    with open('users.json', 'w') as file:
        json.dump(users_data, file, indent=4)

# Signup new user
def signup_user(email, password):
    users_data = read_users_from_file()

    # Check if user already exists
    for user in users_data:
        if user['email'] == email:
            return False, "User already exists."

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Add new user
    new_user = {"email": email, "password": hashed_password}
    users_data.append(new_user)
    write_users_to_file(users_data)
    return True, "Signup successful."



# Check user credentials and perform login
def login_user(email, password):
    users_data = read_users_from_file()

    for user in users_data:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode(), user['password'].encode()):
                return True
            else:
                return False

    return False


# Example usage


@app.route("/")
def home():
    return redirect(url_for('welcome'))

@app.route("/signup")
def signup():
    return render_template("vsignup.html")

@app.route("/login")
def login():
    return render_template("vlogin.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/welcome")
def welcome():
    session_user_id = session.get('authx_email_session')
    cookie_user_id = request.cookies.get('authx-email_cookie')

    print(session_user_id,"session")
    print(cookie_user_id,"cookie")

    if session_user_id != None:
        user_email = session_user_id
    elif cookie_user_id != None:
        user_email = cookie_user_id
    else:
        user_email = " "

    if session_user_id or cookie_user_id:
        return render_template("welcome.html",email=user_email)
    else:
        return redirect('/login')
@app.route("/signupreq",methods=["GET","POST"])
def imgToText():
    if request.method == "POST":
        email = request.form.get("email")
        passw= request.form.get("pass")
        cpassw=request.form.get("cpass")
        tandc=request.form.get("tandc")
        print(tandc)
        if tandc == "on":
            if passw==cpassw:
                success, message = signup_user(email, passw)
                if success:
                    return redirect(url_for('login'))
                else:
                    return render_template("error.html")
            else:
                return render_template("vsignup.html",error_msg="your password and confirm password doesn't match.")

        else:
            return render_template("vsignup.html",error_msg="Please click on the checkbox to login.")

@app.route("/loginreq",methods=["GET","POST"])
def loginreq():
    if request.method == "POST":
        email = request.form.get("email")
        passw= request.form.get("pass")
        stay=request.form.get("stay")
        if login_user(email, passw):
            if stay == 'on':
                # response = make_response(redirect(url_for('welcome',email=email)))
                response = make_response(redirect(url_for('welcome')))
                response.set_cookie('authx-email_cookie',email)
                return response
            else:
                # After successful login
                session['authx_email_session'] = email
                # return redirect(url_for('welcome',email=email))
                return redirect(url_for('welcome'))
        else:
            return render_template("vlogin.html",error_msg="Email or Password are incorrect.")
    else:
        return render_template("error.html")
@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('login')))
    response.set_cookie('authx-email_cookie', '', expires=0)
    return response

app.run(debug=True)