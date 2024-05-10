import mysql.connector

# MySQL 서버 연결 정보
config = {
    'host': 'localhost', 
    'user': 'root',
    'password': '7462',
    'database': 'footprint'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()