import db
import json
import datetime
import requests
#import logging

def get_forecast_from_vendor():
    #logging.basicConfig()
    #logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    forecast = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=5097773&APPID=28f1e52bf99879940247f373318f70e5")
    forecast_data= forecast.content.decode("utf-8")
    forecast_obj=json.loads(forecast_data)
    if forecast_obj["cod"]=="200":
        location="Fair Lawn, NJ"
        currentDT = str(datetime.datetime.now())
        #print(forecast_data)
        conn = db.open()
        cursor = conn.cursor()
        query =(
            "insert into weather_forecast (recorded_time,location, forecast_data) "
            " select %s, %s, %s; "
            )
        cursor.execute(query,(currentDT,location, forecast_data))
        conn.commit()
        if "list" in forecast_obj:
            for hourly_forecast in forecast_obj["list"]:
                forecast_date=hourly_forecast["dt_txt"]
                query =(
                    "insert into weather_forecast_hourly (recorded_time,location, forecast_date,forecast_data) "
                    " select %s, %s, %s,%s; "
                    )
                cursor.execute(query,(currentDT,location, forecast_date, json.dumps(hourly_forecast)))
                conn.commit()
                
                
        cursor.close()
        conn.close()
        
    return 1

s = get_forecast_from_vendor()

    