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
        json_obj=request.get_json()
        #print(json_obj)
        if request.method == 'POST':
            resp=photo.folder_scan('/mnt/d/pic'+json_obj.get('body','/'))
            return resp
    @flask_app.route('/api/photo/<path:path>', methods=['GET'])
    def photo_get_file(path):
            path = path.replace('../','')
            print('/mnt/d/pic/'+ path)
            return photo.get_file('/mnt/d/pic/'+ path)



