"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import functools
from flask import Flask
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
        cur.execute('select UserEmail from user where UserEmail = %s', [useremail])
        p = cur.fetchone()

        if p is None:
            error = 'Incorrect username.'

        cur.execute('select UserPassword, UserEmail from user where UserEmail = %s', [useremail]) #https://stackoverflow.com/questions/69477885/check-password-hash-is-not-working-in-flask-mysql
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

@app.route("/home")
def home():
    return render_template('auth/home.html')

@app.before_request
def load_logged_in_user():
    conn = mysql.connection
    cur = conn.cursor()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cur.execute(
            'SELECT UserEmail FROM user WHERE UserEmail = %s', (user_id,)
        )
        g.user = cur.fetchone()
      
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
                

        cur.execute("SELECT CarID FROM ad WHERE CarID = %s", [carid])
        x = cur.fetchone()
        if x is not None:
            error = f"Car of serial number {carid} is already registered. Did you mean to update your ad?"

        if error is None:

            cur.execute("SELECT RoleId FROM user WHERE UserEmail = %s", [user_id])
            u = cur.fetchone()
            usrole = str(u[0])
            print(usrole)

            try:
                           

                if usrole == "seller":
                    print(usrole)
                    cur.execute(                        
                        "INSERT INTO Ad (Wanted, CarID, PosterID, Price,Used, CarModel,CarColour) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        ("n", carid, user_id, price, carused, carmodel, carcolour),
                    )
                conn.commit()
                


                if usrole == "buyer":
                    print(usrole)
                    cur.execute(                        
                        "INSERT INTO Ad (Wanted, CarID, PosterID, Price,Used, CarModel,CarColour) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        ("y", carid, user_id, price, carused, carmodel, carcolour),
                    )
                conn.commit()



            #except:
             #   cur.execute("SELECT CarId FROM car WHERE CarId = %s", [carid])
              #  x = cur.fetchone()
               # if x is not None:
                #    error = f"Car of serial number {carid} is already registered. Did you mean to update your ad?"


            finally:
                return redirect(url_for('home'))
        flash(error)           

    return render_template('auth/create.html')


#def get_post(id, check_author=True):
 #   post = get_db().execute(
  #      'SELECT p.id, title, body, created, author_id, username'
   #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #    ' WHERE p.id = ?',
     #   (id,)
   # ).fetchone()

    #if post is None:
     #   abort(404, f"Post id {id} doesn't exist.")

    #if check_author and post['author_id'] != g.user['id']:
     #   abort(403)

#    return post


#@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
#def update(id):
 #   post = get_post(id)

  #  if request.method == 'POST':
   #     title = request.form['title']
    #    body = request.form['body']
     #   error = None
     #
       # if not title:
#            error = 'Title is required.'

 #       if error is not None:
  #          flash(error)
   #     else:
    #        db = get_db()
     #       db.execute(
      #          'UPDATE post SET title = ?, body = ?'
       #         ' WHERE id = ?',
        #        (title, body, id)
         #   )
           # db.commit()
          #  return redirect(url_for('blog.index'))

   # return render_template('blog/update.html', post=post)


#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
#def delete(id):
#    get_post(id)
 #   db = get_db()
  #  db.execute('DELETE FROM post WHERE id = ?', (id,))
   # db.commit()
    #return redirect(url_for('blog.index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080') #Run the flask app at port 8080