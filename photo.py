# encoding: cp866
import os
import json
from flask import Response, send_file

def folder_scan(path):
    respObj={}
    respObj["status"]="ok"
    dataObj=[]
    if os.path.isdir(path):
        with os.scandir(path) as entries:
            for entry in entries:
                dataItem={}
                dataItem["name"]=str(entry.name)
                dataItem["isFolder"]=entry.is_dir()
                dataObj.append(dataItem)
        respObj["data"]=dataObj
        resp = json.dumps(respObj, ensure_ascii=False)
        return Response(resp, mimetype='text/json')
    else:
        return Response('', mimetype='text/json')
    
def get_file(path):
    return send_file(path, mimetype='image/jpg')