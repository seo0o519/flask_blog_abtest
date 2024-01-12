import pymysql

MYSQL_HOST = 'localhost'
MYSQL_CONN = pymysql.connect(
    host=MYSQL_HOST,
    port=3306,
    user='root',
    passwd='dianne4746@',
    db='blog_db',
    charset='utf8'
)

def conn_mysqldb(): # mysql 연결
    if not MYSQL_CONN.open: # 연결 끊어졌는지 체크
        MYSQL_CONN.ping(reconnect=True)
    return MYSQL_CONN
