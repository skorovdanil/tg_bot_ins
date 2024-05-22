import sqlite3
conn = sqlite3.connect('db/installation.db')
cursor = conn.cursor()
cursor.execute('SELECT day FROM schedules WHERE worker_id = ?', (685414448,))
result = cursor.fetchall()
conn.close()
values = [item[0] for item in result]
tt = list(set(values))

if "Среда" in tt:
    print(1)