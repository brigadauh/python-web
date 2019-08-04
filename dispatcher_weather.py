from functools import wraps
from flask import jsonify,Response, request
import os
import datetime
import os.path
import db
import json
import requests
import dispatcher
import temphumidity
import forecast
import testviews
import temphumidity_view








def dispatch(flask_app,path):
    

    ##################### weather data
    @flask_app.route('/api/weather/temphumidity/add', methods=['POST','DELETE'])
    def temphumidity_handler_process():
        return temphumidity.add_delete()

    @flask_app.route('/api/weather/temphumidity/current', methods=['POST','GET'])
    def temphumidity_handler_current():
        return temphumidity.get_current()

    @flask_app.route('/api/weather/forecast', methods=['POST','GET'])
    def forecast_handler():
        return forecast.get_latest()

    #@flask_app.route('/api/weather/vendorforecast', methods=['POST','GET'])
    #def vendor_forecast_handler():
    #    resp=utils.getforecast.get_forecast_from_vendor()
    #    return Response(resp, mimetype='text/json')
    
   