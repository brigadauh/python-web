from flask import request,Response, render_template, flash, url_for, redirect, jsonify
from flask_httpauth import HTTPBasicAuth

import os
import datetime
import os.path
import db
import json

def hello_world():
    return Response(
        'Hello world from Flask view\n',
        mimetype='text/plain'
    )
def user_handler():
    resp='["status":"ok", data[{"page_status":"testview construction",version":"0.0"}]'
    return Response(resp, mimetype='text/json')
def user_list_handler():
    conn = db.open()
    cursor = conn.cursor()
    
    query =("select username,password from user "
            "where username=%s and password=%s;")
    username="petya"
    password="qwerty"
    date=datetime.date(2000,12,31)
    
    cursor.execute(query, (username, password))
    data=[]
    for (username, password) in cursor:
      d="{0},  {1}".format(username, password)
      data.append(d)
    cursor.close()
    data_json = json.dumps(data)
    resp='["status":"ok", data['+data_json+']'
    return Response(resp, mimetype='text/json')

