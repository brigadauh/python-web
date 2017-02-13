from flask import Flask
from flask import Response
from flask import request
import os
import datetime
import db
from dispatcher import dispatch

#from mysql.connector import errorcode


##def auth()
conn = db.open()
cursor = conn.cursor()

query =("select username,password from user "
        "where username=%s and password=%s;")
username="petya"
password="qwerty"
date=datetime.date(2000,12,31)

cursor.execute(query, (username, password))
for (username, password) in cursor:
  print("user: {}, pwd: {} ".format(
    username, '****'))
    
cursor.close()

##db.close(conn)


flask_app=Flask(__name__, static_url_path='', static_folder='public')
dispatch(flask_app,'')

app = flask_app.wsgi_app
