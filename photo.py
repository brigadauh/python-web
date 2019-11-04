# encoding: cp866
import os
import json
import db

from flask import Response, send_file

def get_folder_access(token):
    if token == '':
        return ''
    
    conn = db.open()
    cursor = conn.cursor()
    args = [token]
    cursor.callproc('api_get_folder_access', args)
    # print(cursor.fetchone);
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    root_path=''
    for row in rows:
        root_path=row[0]
    return root_path


def folder_scan(path, token):
    respObj={}
    root_path = get_folder_access(token)
    if  root_path == '':
        respObj["status"]="failed"
        return Response(json.dumps(respObj, ensure_ascii=False), mimetype='text/json')
    else:
        respObj["status"]="ok"
    
    dataObj=[]
    path = '/mnt/d/pic'+root_path+path
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
    
def get_file(path, token):
    root_path = get_folder_access(token)
    if  root_path == '':
        path = ''
    else :
        if not root_path.endswith('/'):
            root_path = root_path+ '/'
        path = '/mnt/d/pic' + root_path  + path
    print('file path:***************', path)
    return send_file(path, mimetype='image/jpg')