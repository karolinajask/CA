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
        cur.execute('select UserPassword, UserEmail from user where UserEmail = %s', [useremail]) #https://stackoverflow.com/questions/69477885/check-password-hash-is-not-working-in-flask-mysql
        data = cur.fetchall()
        for row in data:
            hashed_password = ("%s" % (row[0]))
            userid = ("%s" % (row[1]))

        if len(data) > 0:
            if check_password_hash(hashed_password,password):

                return 'logged in successfully'
                #return redirect(url_for('home'))

        flash(error)

    return render_template('auth/login.html')


#@app.before_request
#def load_logged_in_user():
#    useremail = session.get('useremail')
#
 #   if useremail is None:
  #      g.user = None
   # else:
    #    g.user =  cur.execute(
     #       'SELECT * FROM user WHERE UserEmail = ?', (usermemail,)
      #  ).fetchone()
      #
#@app.route('/logout')
#def logout():
 #   session.clear()
  #  return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080