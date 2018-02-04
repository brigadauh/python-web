import db
import json
import datetime
import requests
import temphumidity


def get_current_from_station():
    #current_weather_str='{"coord":{"lon":-74.13,"lat":40.94},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"base":"stations","main":{"temp":277.35,"pressure":1024,"humidity":70,"temp_min":273.15,"temp_max":280.15},"visibility":16093,"wind":{"speed":1.16,"deg":108.002},"clouds":{"all":1},"dt":1512263700,"sys":{"type":1,"id":1969,"message":0.1755,"country":"US","sunrise":1512302650,"sunset":1512336518},"id":5097773,"name":"Fair Lawn","cod":200}'
    #weather_obj=json.loads(current_weather_str)
    weather = requests.get("http://api.openweathermap.org/data/2.5/weather?id=5097773&APPID=28f1e52bf99879940247f373318f70e5")
    weather_data= weather.content.decode("utf-8")
    weather_obj=json.loads(weather_data)

    weather_main=weather_obj["main"]
    tempC=weather_main["temp"]-273
    pressureGPa=weather_main["pressure"]
    humidity=weather_main["humidity"]
    dataObj={}
    dataObj["t"]=tempC
    dataObj["h"]=humidity
    dataObj["d"]= str(datetime.datetime.now())
    return temphumidity.add(dataObj)

s = get_current_from_station()