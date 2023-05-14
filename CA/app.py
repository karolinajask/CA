"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template
from flask import request, current_app, g, session, flash, redirect, render_template, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
from werkzeug.security import check_password_hash, generate_password_hash
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations
app.config['MYSQL_USER'] = 'kjdb'
app.config['MYSQL_PASSWORD'] = 'Karolinadb123!'
app.config['MYSQL_DB'] = 'ca'
app.config['MYSQL_HOST'] = 'kjdb.mysql.database.azure.com' #for now
app.config['SECRET_KEY'] = "GDtfD^&$%@^8tgYjD"
mysql.init_app(app)

@app.route("/")
def index():
    return render_template('base.html')

@app.route('/register', methods=('GET', 'POST'))
def register():    	
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        userfirstname = request.form['userfirstname']
        userlastname = request.form['userlastname']
        cur = mysql.connection.cursor()   
        error = None

        if not useremail:
            error = 'User email is required.'
        if not password:
            error = 'Password is required.'
        if not userfirstname:
            error = 'User First Name is required.'
        elif not userlastname:
            error = 'User Last Name is required.'

        if error is None:
            try:
                cur.execute(
                    "INSERT INTO User (UserEmail, UserPassword, UserFirstName, UserLastName) VALUES (%s, %s, %s, %s)",
                    (useremail, generate_password_hash(password),userfirstname, userlastname),
                )
                mysql.connection.commit()
            except:
                cur.execute("SELECT * FROM User WHERE UserEmail = %s", [useremail])
                error = f"Email {useremail} is already registered."
            else:
                return redirect(url_for("login"))
        flash(error)

    return render_template('auth/register.html')

################################

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        cur = mysql.connection.cursor()
        error = None
        user = cur.execute(
            'SELECT * FROM user WHERE UserEmail = %s', (useremail,)
        ).fetchone()

        if useremail is None:
            error = 'Incorrect User Email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@app.before_request
def load_logged_in_user():
    useremail = session.get('useremail')

    if useremail is None:
        g.user = None
    else:
        g.user =  cur.execute(
            'SELECT * FROM user WHERE UserEmail = ?', (usermemail,)
        ).fetchone()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080