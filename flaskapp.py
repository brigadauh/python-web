from dispatcher import dispatch
from dispatcher_schedule import dispatch as dispatch_schedule
from dispatcher_weather import dispatch as dispatch_weather
from dispatcher_photo import dispatch as dispatch_photo
from flask import Flask, render_template
import os
import datetime
import db

#from mysql.connector import errorcode


##def auth()
conn = db.open()
cursor = conn.cursor()

query =("select username,password from user "
        "where username=%s and password=%s;")
username = "petya"
password = "qwerty"
date = datetime.date(2000,12,31)

cursor.execute(query, (username, password))
for (user, pwd) in cursor:
  print("user: {}, pwd: {} ".format(
    user, '****'))
    
cursor.close()

##db.close(conn)


flask_app = Flask(__name__, static_url_path='', static_folder='public')
#app = flask_app.wsgi_app
dispatch(flask_app,'')
dispatch_schedule(flask_app,'')
dispatch_weather(flask_app,'')
dispatch_photo(flask_app,'')
flask_app.run(host='192.168.1.3', port=int(os.environ.get("PORT", 8888)))
