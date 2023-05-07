"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template
from flask import request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json
mysql = MySQL()
app = Flask(__name__)
CORS(app)
# My SQL Instance configurations
# Change the HOST IP and Password to match your instance configurations
app.config['MYSQL_USER'] = 'web'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cadb'
app.config['MYSQL_HOST'] = 'localhost' #for now
mysql.init_app(app)

#@app.route("/add") #Add Student
#def add():
#  name = request.args.get('name')
#  email = request.args.get('email')
#  cur = mysql.connection.cursor() #create a connection to the SQL instance
#  s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
#  cur.execute(s)
#  mysql.connection.commit()

#  return '{"Result":"Success"}'
#@app.route("/") #Default - Show Data
#def hello(): # Name of the method
#  cur = mysql.connection.cursor() #create a connection to the SQL instance
#  cur.execute('''SELECT * FROM students''') # execute an SQL statment
#  rv = cur.fetchall() #Retreive all rows returend by the SQL statment
#  Results=[]
#  for row in rv: #Format the Output Results and add to return string
#    Result={}
#    Result['Name']=row[0].replace('\n',' ')
#    Result['Email']=row[1]
#    Result['ID']=row[2]
#    Results.append(Result)
#  response={'Results':Results, 'count':len(Results)}
#  ret=app.response_class(
#    response=json.dumps(response),
#    status=200,
#    mimetype='application/json'
#  )
#  return ret #Return the data in a string format

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/')
@app.route('/index/')
@app.route('/index/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

