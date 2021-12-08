from flask import Flask, render_template, request, redirect, session
import mysql.connector
from decouple import config
from sentiments import second
import os

host = config("db_host")
user = config("user_name")
password = config("db_pwd")
db_name = config("db_name")
port = config("db_port")

app = Flask(__name__)

# initializing the user cookie
app.secret_key = os.urandom(24)

# blueprint to call the second python file in the project.
app.register_blueprint(second)


# establishing a connection with mysql database
try:
    conn = mysql.connector.connect(
        host=host, user=user, password=password, database=db_name, port=port
    )
    cursor = conn.cursor()
except:
    print("An error occurred")


# call the login template
@app.route('/')
def login():
    return render_template('login.html')

# call the register template
#
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    passwd = request.form.get('password')

    cursor.execute(
        """SELECT * FROM `users` WHERE `email` LIKE '{}' `PASSWORD` LIKE '{}'""".format(email, passwd)
    )
    users = cursor.fetchall()
    # check if a user has already logged in
    if len(users) > 0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/add_user', methods=['POST'])
def add_user():
    # get user login data and pass the data to database
    name = request.form.get('uname')
    email = request.form.get('uemail')
    pwd = request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`name`, `email`, `password`) VALUES ('{}', '{}', '{}'""".format(
        name, email, pwd
    ))
    conn.commit()
    cursor.execute(
        """SELECT * from `users` WHERE `email` LIKE '{}'""".format(email)
    )
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    # close the session
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

