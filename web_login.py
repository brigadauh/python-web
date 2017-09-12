from flask import jsonify,Response, request
import db
import json
import datetime

def authenticate():
    json_obj=request.get_json()
    username=''
    password=''
    if request.method == 'POST':
        username=json_obj.get('username','')
        password=json_obj.get('password','')
    return db.verify_credentials(username,password)
    
