import sqlite3
from collections import defaultdict
from datetime import datetime

conn = sqlite3.connect('installation.db')
cursor = conn.cursor()
day = "Понедельник"
cursor.execute("""
    SELECT schedules.worker_id,schedules.id, schedules.time, schedules.day, worker.name, worker.region, worker.id
    FROM schedules
    INNER JOIN worker ON schedules.worker_id = worker.telegram_id
    WHERE schedules.day = ? and schedules.installation != True
""", (day,))
data = cursor.fetchall()
conn.close()
print(data)

# Фильтр по дню недели
day = 'Понедельник'
sorted_data = sorted(data, key=lambda x: (x[6], datetime.strptime(x[2].split(' - ')[0], "%H:%M")))
# Группировка данных по пользователям и их значениям
grouped = defaultdict(lambda: defaultdict(list))
for item in sorted_data:
    user = item[4]
    value = item[5]
    time = item[2]
    grouped[user][value].append(time)

output = f"{day}\n\n"
for user in grouped:
    for value in grouped[user]:
        output += f"{user} {value}\n"
        for time in grouped[user][value]:
            output += f"{time}\n"
        output += "\n"  # Пустая строка между группами времени для одного значения

output = output.strip()  # Убираем лишние конечные переносы

print(output)