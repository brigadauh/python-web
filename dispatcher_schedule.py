from functools import wraps
from flask import jsonify,Response, request
import os
import datetime
import os.path
import db
import json
import requests
import dispatcher
import schedule







def dispatch(flask_app,path):
    

    
    ##################### schedule (test)
    @flask_app.route('/api/schedule/list/active')
    def schedule_handler_active():
        resp=schedule.list_active()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/list/processed')
    def schedule_handler_processed():
        resp=schedule.list_processed()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/list/current')
    def schedule_handler_current():
        resp=schedule.list_current()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/list/current3')
    def schedule_handler_current3():
        resp=schedule.list_current()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/add', methods=['POST','DELETE'])
    def schedule_handler_process():
        json_obj=request.get_json()
        if request.method == 'POST':
            resp=schedule.add(json_obj)
            return Response(resp, mimetype='text/json')
        else:
            resp=schedule.delete(json_obj)
            return Response(resp, mimetype='text/json')
    
    