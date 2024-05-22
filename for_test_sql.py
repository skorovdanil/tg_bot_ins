import sqlite3
conn = sqlite3.connect('db/installation.db')
cursor = conn.cursor()
cursor.execute('SELECT day,time FROM schedules WHERE worker_id = ?', (685414448,))
result = cursor.fetchall()
conn.close()

day_order = {
    'Понедельник': 1,
    'Вторник': 2,
    'Среда': 3,
    'Четверг': 4,
    'Пятница': 5,
    'Суббота': 6,
    'Воскресенье': 7
}
# Функция, чтобы извлечь начало временного диапазона в часах и минутах

def get_time_key(time_range):

    start_time = time_range.split(' - ')[0]

    return tuple(map(int, start_time.split(':')))

# Сортировка списка по дням недели и времени

sorted_schedule = sorted(

    result,

    key=lambda entry: (day_order[entry[0]], get_time_key(entry[1]))

)

# Создание словаря для группировки по дням недели

grouped_schedule = {}

for day, time in sorted_schedule:

    if day not in grouped_schedule:

        grouped_schedule[day] = []

    grouped_schedule[day].append(time)

# Преобразование словаря в список списков

result = [[day] + times for day, times in grouped_schedule.items()]

lines = []



# Проход по каждому дню в данных

for days in result:

    day = days[0]  # Первый элемент - день недели
    lines.append(day)  # Добавляем день недели в список строк
    for i in range(1, len(days)):  # Проход по временам
        time = days[i]
        lines.append(time)  # Добавляем временной интервал в список строк
    lines.append('')  # Добавляем пустую строку для разделения дней



# Объединение всех строк в один текст, удаляя последнюю пустую строку

final_text = '\n'.join(lines).strip()



print(final_text)
