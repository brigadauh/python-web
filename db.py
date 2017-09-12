import mysql.connector

mysqlConfig = {
  'user': 'sapi_admin',
  'password': '',
  'host': '192.168.1.3',
  'database': 'sapi',
  'raise_on_warnings': False,
  'pool_name': 'sapi_pool',
  'pool_size':5
}
def open():
    ##subsequent calls to this will return connections from the same pool
    cnx = mysql.connector.connect(**mysqlConfig)
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

    args = [username, password]
    cursor.callproc('api_login', args)
    uuid=''
    for (uid) in cursor:
      uuid=uid
    cursor.close()
    if (uuid == '' ):
        return ''
    else:
        return uuid        
