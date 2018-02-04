from flask import jsonify,Response, request
import db
import json
import datetime

def add_delete():
    json_obj=request.get_json()
    if request.method == 'POST':
        resp=add(json_obj)
        return Response(resp, mimetype='text/json')
    else:
        resp=delete(json_obj)
        return Response(resp, mimetype='text/json')

def add(data):
    temp=data.get('t','')
    humidity=data.get('h','')
    time=data.get('d','')
    #print (temp, humidity, time)
    conn = db.open()
    cursor = conn.cursor()
    query =("insert into weather_data " 
            "(recorded_time,temp,humidity)"
            " select %s, %s, %s; "
           )
    
    cursor.execute(query,(time, temp, humidity))
    conn.commit()
    var_task_id=cursor.lastrowid
    cursor.close()
    conn.close()

    respObj={}
    respObj["status"]="ok"
    dataObj={}
    dataObj["id"]=var_task_id
    respObj["data"]=dataObj

    return json.dumps(respObj)

    
    

def delete(data):
    return '{"status":"failed", "err":"not implemented","data":[]}'

def get_current():
    json_obj=request.get_json()
    
    conn = db.open()
    cursor = conn.cursor()
    query =("select recorded_time,temp,humidity, (SELECT temp FROM weather_data WHERE recorded_time < DATE_ADD(w.`recorded_time`, INTERVAL -30 MINUTE) ORDER BY recorded_time DESC LIMIT 1) AS recent_temp "
            " FROM weather_data w order by recorded_time desc limit 1;")
    cursor.execute(query)
    respObj={}
    respObj["status"]="ok"
    dataObj=[]

    for (var_recorded_time, var_temp, var_humidity, var_recent_temp) in cursor:
        print("time: {}, temp: {}, humidity: {}, recent temp: {}".format(
        var_recorded_time, var_temp, var_humidity, var_recent_temp))
        dataItem={}
        dataItem["recorded_time"]=str(var_recorded_time)
        dataItem["temp"]=str(var_temp)
        dataItem["humidity"]=str(var_humidity)
        dataItem["recent_temp"]=str(var_recent_temp)
        dataObj.append(dataItem)

    respObj["data"]=dataObj
    cursor.close()
    conn.close()
    return Response(json.dumps(respObj), mimetype='text/json')
