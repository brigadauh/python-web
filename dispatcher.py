from functools import wraps
from flask import jsonify,Response, request
import os
import datetime
import os.path
import db
import json
import requests
import testviews

import web_login
import schedule
import api_response
import photo
#import utils.getforecast


def getUser(cookie):
    conn = db.open()
    cursor = conn.cursor()
    
    query =("select username from user_cookie "
            "where cookie = %(cookie_value)s")

    cursor.execute(query, {"cookie_value":cookie})
    user=False
    for (username) in cursor:
      user=username
    cursor.close()
    return user



def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ret='{"status":"failed", "err":"authentication required","data":[]}'
        cookie = request.cookies.get('api_cookie')
        if cookie:
            user = getUser(cookie)
            if user:
                # Success!
                #return render_template('welcome.html', user=user)
                ret= f(*args, **kwargs)
        return ret 
        
        #username = "admin"
        #password="secret"
        #if not check_auth(username, password):
        #    return authenticate()
        #return f(*args, **kwargs)
        
    return decorated

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))+'/public/'
def get_file(filename):  # pragma: no cover
    print(filename)
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)
default_page='index.html'

def dispatch(flask_app,path):
    

        
   
    
    ####################### PHOTO ALBUM
    @flask_app.route('/api/photo', methods=['POST'])
    def photo_folder_scan():
        json_obj=request.get_json()
        #print(json_obj)
        if request.method == 'POST':
            resp=photo.folder_scan('/mnt/d/pic'+json_obj.get('body','/'))
            return resp
    @flask_app.route('/api/photo/<path:path>', methods=['GET'])
    def photo_get_file(path):
            path = path.replace('../','')
            print('/mnt/d/pic/'+ path)
            return photo.get_file('/mnt/d/pic/'+ path)



    ########################## CHAT
    @flask_app.route('/api/chat/users', methods=['POST'])
    def chat_users():
        json_obj=request.get_json()
        resp=chat.get_users();
        return Response(resp, mimetype='text/json')
    
    

    ########################## default page
    
    @flask_app.route('/root')
    @requires_auth
    def root():
        return Response(
            'root:' + root_dir(),
            mimetype='text/plain'
        )
    @flask_app.route('/api/login', methods=['POST'])
    def login():
        uuid= web_login.authenticate()
        resp=api_response.responseErr('login_failed','Incorrect Username/Password')
        print(uuid)
        if (uuid!=''):
            resp=api_response.responseOK()
        response=Response(resp, mimetype='text/json')
        if (uuid!=''):
            response.set_cookie('api_cookie',value=uuid)
        return response
    @flask_app.route('/api/create-account', methods=['POST'])
    def create_acc():
        uuid= web_login.create_account()
        resp='{"status":"failed"}'
        if (uuid!=''):
            resp='{"status":1}'
        response=Response(resp, mimetype='text/json')
        if (uuid!=''):
            response.set_cookie('api_cookie',value=uuid)
        return response
    
    
    
    
    
    # ##################### schedule (test)
    # @flask_app.route('/api/schedule/list/active')
    # def schedule_handler_active():
    #     resp=schedule.list_active()
    #     return Response(resp, mimetype='text/json')
    # @flask_app.route('/api/schedule/list/processed')
    # def schedule_handler_processed():
    #     resp=schedule.list_processed()
    #     return Response(resp, mimetype='text/json')
    # @flask_app.route('/api/schedule/list/current')
    # def schedule_handler_current():
    #     resp=schedule.list_current()
    #     return Response(resp, mimetype='text/json')
    # @flask_app.route('/api/schedule/add', methods=['POST','DELETE'])
    # def schedule_handler_process():
    #     json_obj=request.get_json()
    #     if request.method == 'POST':
    #         resp=schedule.add(json_obj)
    #         return Response(resp, mimetype='text/json')
    #     else:
    #         resp=schedule.delete(json_obj)
    #         return Response(resp, mimetype='text/json')
    # 
    # 

    ########################## various tests
    flask_app.add_url_rule('/hello', 'hello', view_func=testviews.hello_world)
    flask_app.add_url_rule('/api/user', 'user', view_func=testviews.user_handler)
    flask_app.add_url_rule('/api/user/list', 'user_list_handler', view_func=testviews.user_list_handler)

    @flask_app.route('/', defaults={'path': root_dir()+'/'+default_page})
    

    @flask_app.route('/<path:path>')
    def get_resource(path):  # pragma: no cover
        mimetypes = {
            ".css": "text/css",
            ".html": "text/html",
            ".js": "application/javascript",
        }
        complete_path = os.path.join(root_dir(), path)
        ext = os.path.splitext(path)[1]
        if (ext==''):
            ext=os.path.splitext(default_page)[1]
            complete_path=complete_path+'/'+default_page
        mimetype = mimetypes.get(ext, "text/html")
        content = get_file(complete_path)
        return Response(content, mimetype=mimetype)
    #@flask_app.route('/<name>')
    #def hello_name(name):
    #    return "Hello {}!".format(name)

    
