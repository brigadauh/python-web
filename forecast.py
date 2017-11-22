from flask import jsonify,Response, request
import db
import json
import datetime

def get_latest():
    json_obj=request.get_json()
    
    conn = db.open()
    cursor = conn.cursor()
    query =("select recorded_time,forecast_data from weather_forecast "
            "order by recorded_time desc limit 1;")
    cursor.execute(query)
    respObj={}
    respObj["status"]="ok"
    dataObj=[]

    for (var_recorded_time, var_forecast_data) in cursor:
        #print("time: {}, data: {}".format(
        #var_recorded_time, var_forecast_data))
        dataItem={}
        dataItem["recorded_time"]=str(var_recorded_time)
        dataItem["forecasts"]=json.loads(var_forecast_data)
        dataObj.append(dataItem)

    respObj["data"]=dataObj
    cursor.close()
    conn.close()
    return Response(json.dumps(respObj), mimetype='text/json')
