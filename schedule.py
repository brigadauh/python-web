import db
import json
import datetime

def list_active():
    conn = db.open()
    cursor = conn.cursor()
    query =("select task_id,name,description, exec_method, exec_date from scheduled_tasks "
            "where exec_date > NOW() order by exec_date;")
    cursor.execute(query)
    resp='['
    comma=''
    for (var_task_id, var_name, var_description, var_exec_method, var_exec_date ) in cursor:
      print("task: {}, name: {}, description: {}, method: {}, time: {} ".format(
        var_task_id, var_name, var_description, var_exec_method, var_exec_date))
      resp=resp+comma+'{"task_id": "'+str(var_task_id)+'","name": "'+var_name+'", "description":"'+var_description+'","exec_method": "'+var_exec_method+'","exec_date": "'+str(var_exec_date)+'"}'
      comma=','
      #print("{}, {} was hired on {:%d %b %Y}".format(
      #  last_name, first_name, hire_date))
    resp=resp+']'
    cursor.close()
    return resp

def list_processed():
    conn = db.open()
    cursor = conn.cursor()
    query =("select task_id,name,description, exec_method, exec_date from scheduled_tasks "
            "where exec_date <= NOW() and status=1 order by exec_date desc;")
    cursor.execute(query)
    resp='['
    comma=''
    for (var_task_id, var_name, var_description, var_exec_method, var_exec_date ) in cursor:
      print("task: {}, name: {}, description: {}, method: {}, time: {} ".format(
        var_task_id, var_name, var_description, var_exec_method, var_exec_date))
      resp=resp+comma+'{"task_id": "'+str(var_task_id)+'","name": "'+var_name+'", "description":"'+var_description+'","exec_method": "'+var_exec_method+'","exec_date": "'+str(var_exec_date)+'"}'
      comma=','
      #print("{}, {} was hired on {:%d %b %Y}".format(
      #  last_name, first_name, hire_date))
    resp=resp+']'
    cursor.close()
    return resp

def list_current():
    conn = db.open()
    cursor = conn.cursor()
    query =("select task_id,name,description, exec_method, exec_date from scheduled_tasks "
            "where exec_date <= NOW() and status=0 order by exec_date desc;")
    cursor.execute(query)
    resp='['
    comma=''
    for (var_task_id, var_name, var_description, var_exec_method, var_exec_date ) in cursor:
      print("task: {}, name: {}, description: {}, method: {}, time: {} ".format(
        var_task_id, var_name, var_description, var_exec_method, var_exec_date))
      resp=resp+comma+'{"task_id": "'+str(var_task_id)+'","name": "'+var_name+'", "description":"'+var_description+'","exec_method": "'+var_exec_method+'","exec_date": "'+str(var_exec_date)+'"}'
      comma=','
      #print("{}, {} was hired on {:%d %b %Y}".format(
      #  last_name, first_name, hire_date))
    resp=resp+']'
    cursor.close()
    return resp

def add(data):
    name=data.get('name','')
    description=data.get('description','')
    exec_method=data.get('exec_method','')
    exec_date=data.get('exec_date',datetime.datetime.now().strftime("%Y-%m-%d"))
    status='0'
    conn = db.open()
    cursor = conn.cursor()
    query =("insert into scheduled_tasks " 
            "(name,description, exec_method, exec_date, status)"
            " select %s, %s, %s, %s, %s; "
           )
    
    cursor.execute(query,(name, description, exec_method, exec_date, status))
    conn.commit()
    conn.close()
    var_task_id=cursor.lastrowid
    resp='{"status":"ok","data":[{"task_id": "'+str(var_task_id)+'"}]'
    cursor.close()
    return resp
def delete(data):
    task_id=data.get('task_id','')
    conn = db.open()
    cursor = conn.cursor()
    query =("delete from scheduled_tasks " 
            " where task_id=%s; "
           )
    cursor.execute(query, (task_id))
    conn.commit()
    conn.close()
    resp='{"status":"ok","data":[]'
    return resp

