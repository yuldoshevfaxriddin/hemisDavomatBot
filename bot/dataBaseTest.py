import sqlite3

conn = sqlite3.connect("us-cdbr-east-06.cleardb.net")
print(conn)

cur = conn.cursor()
print(cur.execute('SHOW TABLES FROM database_name;'))

