from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/api/schedule/add',methods=['POST'])
def schedule_add():
    resp=request.form['name']
    print ('resp', resp)
    return 'Hello, schedule!'+resp
@app.route('/api/schedule/add_json',methods=['POST'])
def schedule_add_json():
    resp=request.get_json()
    print ('resp', resp)
    return 'Hello, json!'+resp["name"]

