from flask import jsonify,Response, request
import os
import datetime
import os.path
import db
import json
import schedule


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
    
    @flask_app.route('/api/schedule/list/active')
    def schedule_handler_active():
        resp=schedule.list_active()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/list/processed')
    def schedule_handler_processed():
        resp=schedule.list_processed()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/list/current')
    def schedule_handler_current():
        resp=schedule.list_current()
        return Response(resp, mimetype='text/json')
    @flask_app.route('/api/schedule/add', methods=['POST','DELETE'])
    def schedule_handler_process():
        json_obj=request.get_json()
        if request.method == 'POST':
            resp=schedule.add(json_obj)
            return Response(resp, mimetype='text/json')
        else:
            resp=schedule.delete(json_obj)
            return Response(resp, mimetype='text/json')
            
    
    
    ########################## default page
    @flask_app.route('/root')
    def root():
        return Response(
            'root:' + root_dir(),
            mimetype='text/plain'
        )
    ########################## test
    @flask_app.route('/hello')
    def hello_world():
        return Response(
            'Hello world from Flask\n',
            mimetype='text/plain'
        )
    @flask_app.route('/api/user')
    def user_handler():
        resp='["status":"ok", data[{"page_status":"construction",version":"0.0"}]'
        return Response(resp, mimetype='text/json')
    
    @flask_app.route('/api/user/list')
    def user_list_handler():
        conn = db.open()
        cursor = conn.cursor()
        
        query =("select username,password from user "
                "where username=%s and password=%s;")
        username="petya"
        password="qwerty"
        date=datetime.date(2000,12,31)
        
        cursor.execute(query, (username, password))
        data=[]
        for (username, password) in cursor:
          d="{0},  {1}".format(username, password)
          data.append(d)
        cursor.close()
        data_json = json.dumps(data)
        resp='["status":"ok", data['+data_json+']'
        return Response(resp, mimetype='text/json')
    
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

    
