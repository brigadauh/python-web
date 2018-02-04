from flask import jsonify,Response, request
import db
import json
import datetime

def get_latest():
    json_obj=request.get_json()
    currentDT = str(datetime.datetime.now())
    conn = db.open()
    cursor = conn.cursor()
    #query =("CALL api_get_forecast_data(%s);")
    #cursor.execute(query,(currentDT))
    args = [currentDT]
    cursor.callproc('api_get_forecast_data', args)
    print(cursor.fetchone);
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    respObj={}
    respObj["status"]="ok"
    dataObj=[]

    for row in rows:
        var_forecast_date=row[0]
        var_forecast_data=row[1]
        dataItem={}
        dataItem["forecast_date"]=str(var_forecast_date)
        dataItem["forecasts"]=json.loads(var_forecast_data)
        dataObj.append(dataItem)

    respObj["data"]=dataObj
    return Response(json.dumps(respObj), mimetype='text/json')
