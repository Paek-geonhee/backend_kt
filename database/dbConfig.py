import mysql
import mysql.connector

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '7462', 
    'database': 'footprint'
}

conn = mysql.connector.connect(**mysql_config) ## '**딕셔너리'는 딕셔너리 언패킹 파이썬 문법(d = {a=1, b=2} -> **d = (1, 2))
cursor = conn.cursor()