# encoding: cp866
import os
import json

def folder_scan(folder):
    respObj={}
    respObj["status"]="ok"
    dataObj=[]
    with os.scandir(folder) as entries:
        for entry in entries:
            dataItem={}
            dataItem["name"]=str(entry.name)
            dataItem["isFolder"]=entry.is_dir()
            dataObj.append(dataItem)
    respObj["data"]=dataObj
    return json.dumps(respObj, ensure_ascii=False)

