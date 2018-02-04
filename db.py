#import mysql.connector
import pymysql

mysqlConfig = {
  'user': 'sapi_admin',
  'password': '',
  'host': '192.168.1.3',
  'database': 'sapi' #,
  #'raise_on_warnings': False ,
  #'pool_name': 'sapi_pool',
  #'pool_size':5
}
def pyTest():
  conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql')
  cur = conn.cursor()
  cur.execute("SELECT Host,User FROM user")
  print(cur.description)
  print()
  for row in cur:
    print(row)

  cur.close()
  conn.close()


def open():
    ##subsequent calls to this will return connections from the same pool
    #cnx = mysql.connector.connect(**mysqlConfig)
    cnx = pymysql.connect(**mysqlConfig)
    return cnx
def close(cnx):
    cnx.close()
## attempt to check connection
def checkConn(self):
    sq = "SELECT NOW()"
    try:
        self.cur.execute( sq )
    except pymysql.Error as e:
        if e.errno == 2006:
            return self.connect()
        else:
            print ( "No connection with database." )
            return False    

def verify_credentials(username,password):
    conn = open()
    cursor = conn.cursor()
    args = (username, password)
    cursor.callproc('api_login', args)
    uuid=''
    result_row=None
    for result in cursor.fetchall_unbuffered()():
      result_row=result.fetchall()
    ##print(result_row[0])
    uuid= result_row[0][0].encode('utf-8')
    cursor.close()
    close(conn)
    return uuid        

def create_user(username,password):
    conn = open()
    cursor = conn.cursor()
    args = (username, password)
    cursor.callproc('api_user_insert', args)
    result_row=None
    for result in cursor.fetchall_unbuffered()():
      result_row=result.fetchall()
    print(result_row[0])
    cursor.close()
    close(conn)
    return result_row[0]        
