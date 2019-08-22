from functools import wraps
from flask import jsonify,Response, request
import os
import datetime
import os.path
import db
import json
import requests
import dispatcher
import photo

def dispatch(flask_app,path):

   ####################### PHOTO ALBUM
    @flask_app.route('/api/photo', methods=['POST'])
    def photo_folder_scan():
        json_obj = request.get_json()
        token = json_obj.get('token','')

        if request.method == 'POST':
            resp=photo.folder_scan(json_obj.get('body',''),token)
            return resp
    @flask_app.route('/api/photo/<path:path>', methods=['GET'])
    def photo_get_file(path):
        token = request.args.get('t', '')
        root_path='/'
        # if 'token' in json_obj.keys():
        #     root_path='/'
        
        path = path.replace('../','')
        return photo.get_file(path, token)



