"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import functools
from flask import Flask
from flask import request, current_app, g, session, flash, redirect, render_template, url_for, abort
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_cors import CORS
import json
from werkzeug.security import check_password_hash, generate_password_hash
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations
app.config['MYSQL_USER'] = 'workbenchuser'
app.config['MYSQL_PASSWORD'] = 'karolina123!'
app.config['MYSQL_DB'] = 'ca'
app.config['MYSQL_HOST'] = '35.228.28.162' #for now
app.config['SECRET_KEY'] = "GDtfD^&$%@^8tgYjD"
mysql.init_app(app)


@app.route('/', methods=('GET','POST'))
def index():
    #creating variable for connection
    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor) 
    #executing query
    cur.execute("select AdId,AdDate, Wanted, Price, Used, CarModel, CarColour from Ad")
    #fetching all records from database
    data=cur.fetchall()
    #returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template("index.html",data=data)


@app.route('/register', methods=('GET', 'POST'))
def register():    	
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        userfirstname = request.form['userfirstname']
        userlastname = request.form['userlastname']
        userrole = request.form['userrole']
        #cur = mysql.connection.cursor()
        conn = mysql.connection
        cur = conn.cursor()  
        error = None

        if not useremail:
            error = 'User email is required.'
        if not password:
            error = 'Password is required.'
        if not userfirstname:
            error = 'User First Name is required.'
        if not userlastname:
            error = 'User Last Name is required.'
        elif not userrole:
            error = 'Please choose if you are a buyer or seller.'

        if error is None:
            try:
                cur.execute(
                    "INSERT INTO User (UserEmail, UserPassword, UserFirstName, UserLastName, RoleId) VALUES (%s, %s, %s, %s, %s)",
                    (useremail, generate_password_hash(password),userfirstname, userlastname, userrole),
                )
                conn.commit()
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
        conn = mysql.connection
        cur = conn.cursor()
        error = None
        cur.execute('select UserEmail from User where UserEmail = %s', [useremail])
        p = cur.fetchone()

        if p is None:
            error = 'Incorrect username.'

        cur.execute('select UserPassword, UserEmail from User where UserEmail = %s', [useremail]) #https://stackoverflow.com/questions/69477885/check-password-hash-is-not-working-in-flask-mysql
        data = cur.fetchall()
        for row in data:
            hashed_password = ("%s" % (row[0]))
            userid = ("%s" % (row[1]))

        if len(data) > 0:
            if check_password_hash(hashed_password,password):

                #return 'logged in successfully'
                
                session.clear()
                session['user_id'] = p[0]
                return redirect(url_for("home"))

            else:
                error = 'Incorrect password.'

        flash(error)

    return render_template('auth/login.html')


@app.before_request
def load_logged_in_user():
    conn = mysql.connection
    cur = conn.cursor()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur.execute(
            'SELECT UserEmail FROM User WHERE UserEmail = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.execute(
            'SELECT UserFirstName FROM User WHERE UserEmail = %s', (user_id,)
        )
        g.name = cur.fetchone()
        

      
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view

@app.route("/home")
@login_required
def home():
    user_id = session.get('user_id')
    #creating variable for connection
    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor) 
    #executing query
    cur.execute("select AdId, AdDate, Wanted, Price, Used, CarModel, CarColour from Ad where PosterID = %s" , (user_id,) )
    #fetching all records from database
    data=cur.fetchall()
    #returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template('auth/home.html',data=data)

########################################################################################################################################
@app.route('/likes', methods=('GET', 'POST'))
@login_required
def likes():

    user_id = session.get('user_id')
    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor) 
    #executing query
    cur.execute("select AdId, AdDate, Wanted, Price, Used, CarModel, CarColour from Ad ")
    #fetching all records from database
    data=cur.fetchall()
    if request.method == 'POST':
        adid = request.form['adid']
        conn = mysql.connection
        cur = conn.cursor() 

        cur.execute(
                    "INSERT INTO Likes (AdId, UserEmail) VALUES (%s, %s)",
                    (adid, user_id),
        )
        conn.commit()
        cur.execute("SELECT * FROM Likes")
        a=cur.fetchall()
        print(a)

        return redirect(url_for('index'))
    return render_template('auth/likes.html',data=data)


@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    user_id = session.get('user_id')
    if request.method == 'POST':
        carid = request.form['carid']
        carused = request.form['carused']
        carmodel = request.form['carmodel']
        carcolour = request.form['carcolour']
        price = request.form['price']
        conn = mysql.connection
        cur = conn.cursor()
        error = None                

        cur.execute("SELECT CarID FROM Ad WHERE CarID = %s", [carid])
        x = cur.fetchone()
        if x is not None:
            error = f"Car of serial number {carid} is already registered. Did you mean to update your ad?"

        if error is None:

            cur.execute("SELECT RoleId FROM User WHERE UserEmail = %s", [user_id])
            u = cur.fetchone()
            usrole = str(u[0])

            try:                          

                if usrole == "seller":
                    cur.execute(                        
                        "INSERT INTO Ad (Wanted, CarID, PosterID, Price,Used, CarModel,CarColour) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        ("n", carid, user_id, price, carused, carmodel, carcolour),
                    )
                conn.commit()

                if usrole == "buyer":
                    cur.execute(                        
                        "INSERT INTO Ad (Wanted, CarID, PosterID, Price,Used, CarModel,CarColour) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        ("y","n/a-wanted", user_id, price, carused, carmodel, carcolour),
                    )
                conn.commit()

            finally:
                return redirect(url_for('home'))
        flash(error)           

    return render_template('auth/create.html')

#################################################################

@app.route('/update', methods=('GET', 'POST'))
@login_required
def update():  
    user_id = session.get('user_id')
    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor) 
    cur.execute("select * FROM Ad where PosterID = %s" , ( user_id,))
    #fetching all records from database
    data=cur.fetchall()
    conn.commit()
           
    if request.method == 'POST':   
        adid = request.form['adid']
        carmodel = request.form['carmodel']
        carcolour = request.form['carcolour']
        price = request.form['price']
        conn = mysql.connection
        cur = conn.cursor()
        error = None

        cur.execute(  "UPDATE Ad SET CarModel = %s, CarColour = %s, Price = %s WHERE AdId = %s" ,
                        (carmodel, carcolour,price,adid,))    
        
        conn.commit()
        return redirect(url_for('home'))

    return render_template('auth/update.html',data=data)
#################################################################

@app.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    user_id = session.get('user_id')
    conn = mysql.connection
    cur = conn.cursor(MySQLdb.cursors.DictCursor) 
    cur.execute("select * FROM Ad where PosterID = %s" , ( user_id,))
    #fetching all records from database
    data=cur.fetchall()
    conn.commit()
           
    if request.method == 'POST':   
        adid = request.form['adid']
        conn = mysql.connection
        cur = conn.cursor()
        error = None

        cur.execute(  "DELETE from Ad WHERE AdId = %s" ,
                        (adid,))   
        print(adid)
        
        conn.commit()

        return redirect(url_for('home'))
    return render_template('auth/delete.html',data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080