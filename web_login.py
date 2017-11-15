from flask import jsonify,Response, request
import db
import json
import datetime

def authenticate():
    username=''
    password=''
    if request.method == 'POST':
        form_obj=request.form
        data_str=form_obj.get('request','')
        data_obj=json.loads(data_str)
        username=data_obj['login']
        password=data_obj['password']
        ret=db.verify_credentials(username,password)
    return ret

def create_account():
    username=''
    password=''
    if request.method == 'POST':
        form_obj=request.form
        data_str=form_obj.get('request','')
        data_obj=json.loads(data_str)
        username=data_obj['login']
        password=data_obj['password']
        ret=db.create_user(username,password)
        status=0
        err=''
        message=''
        uuid=''

        status= ret[0]
        err= ret[1].encode('utf-8')
        message= ret[2].encode('utf-8')
        uuid= ret[3].encode('utf-8')
        
    return uuid
    
