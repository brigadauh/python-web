import requests
#r = requests.post("http://192.168.1.3:8888/api/schedule/add", data={"name":"task1","description":"task 1", "exec_method":"tst_run", "exec_date":"2017-01-01"})
message={"name":"task1","description":"task 1"}
#r = requests.post("http://192.168.1.3:8888/api/schedule/add", data=message)
r = requests.post("http://192.168.1.3:8888/api/schedule/add", json=message)

# And done.
print(r.text) # displays the result body.