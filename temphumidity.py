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
    temp = data.get('t','')
    humidity = data.get('h','')
    time = data.get('d','')
    source = data.get('s','')
    #print (temp, humidity, time)
    conn = db.open()
    cursor = conn.cursor()
    query =("insert into weather_data " 
            "(recorded_time,temp,humidity,source)"
            " select %s, %s, %s, %s;"
           )
    
    cursor.execute(query,(time, temp, humidity, source))
    conn.commit()
    var_task_id=cursor.lastrowid
    cursor.close()
    conn.close()

    respObj={}
    respObj["status"]="ok"
    dataObj={}
    dataObj["id"]=var_task_id
    respObj["data"]=dataObj
    print('temphumidity.add:',json.dumps(respObj))
    return json.dumps(respObj)

    
    

def delete(data):
    return '{"status":"failed", "err":"not implemented","data":[]}'

def get_current():
    json_obj=request.get_json()
    
    conn = db.open()
    cursor = conn.cursor()
    query =("select recorded_time,temp,humidity,"
            " (SELECT temp FROM weather_data WHERE recorded_time < DATE_ADD(w.`recorded_time`, INTERVAL -30 MINUTE) ORDER BY recorded_time DESC, source LIMIT 1) AS recent_temp, source, "
            "(SELECT temp FROM weather_data WHERE source = 'web' AND recorded_time >= DATE_ADD(w.`recorded_time`, INTERVAL -10 MINUTE) ORDER BY recorded_time DESC LIMIT 1) AS temp_web"
            " FROM weather_data w order by recorded_time desc, source limit 1;")
    cursor.execute(query)
    respObj={}
    respObj["status"]="ok"
    dataObj=[]

    for (var_recorded_time, var_temp, var_humidity, var_recent_temp, var_source, var_temp_web) in cursor:
        print("time: {}, temp: {}, humidity: {}, recent temp: {}, web temp: {}".format(
        var_recorded_time, var_temp, var_humidity, var_recent_temp, var_temp_web))
        dataItem={}
        dataItem["recorded_time"]=str(var_recorded_time)
        dataItem["temp"]=str(var_temp)
        dataItem["humidity"]=str(var_humidity)
        dataItem["recent_temp"]=str(var_recent_temp)
        dataItem["source"] = var_source
        dataItem["temp_web"] = str(var_temp_web)
        dataObj.append(dataItem)

    respObj["data"]=dataObj
    cursor.close()
    conn.close()
    return Response(json.dumps(respObj), mimetype='text/json')
