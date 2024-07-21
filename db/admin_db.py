import sqlite3
from datetime import datetime

async def get_schedules_day():
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT day FROM schedules ')
    result = cursor.fetchall()
    conn.close()
    values = [item[0] for item in result]
    days = list(set(values))
    day_order = {
        'Понедельник': 1,
        'Вторник': 2,
        'Среда': 3,
        'Четверг': 4,
        'Пятница': 5,
        'Суббота': 6,
        'Воскресенье': 7
    }
    sorted_days = sorted(days, key=lambda day: day_order[day])
    return sorted_days


async def get_workers_list():
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id,name,region,tel_number FROM worker')
    result = cursor.fetchall()
    conn.close()
    return result


async def get_schedules_worker_info(day):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()


    cursor.execute("""
        SELECT schedules.worker_id,schedules.id, schedules.time, schedules.day, worker.name, worker.region, worker.id
        FROM schedules
        INNER JOIN worker ON schedules.worker_id = worker.telegram_id
        WHERE schedules.day = ? and schedules.installation != True
    """, (day,))
    data = cursor.fetchall()
    not_install_data = sorted(data, key=lambda x: (x[6], datetime.strptime(x[2].split(' - ')[0], "%H:%M")))

    cursor.execute("""
        SELECT schedules.worker_id,schedules.id, schedules.time, schedules.day, worker.name, worker.region, worker.id , schedules.installation
        FROM schedules
        INNER JOIN worker ON schedules.worker_id = worker.telegram_id
        WHERE schedules.day = ?""", (day,))
    data = cursor.fetchall()
    all_install_data = sorted(data, key=lambda x: (x[6], datetime.strptime(x[2].split(' - ')[0], "%H:%M")))
    conn.close()
    return not_install_data, all_install_data

async def reservation_schedule_installation(schedule_id):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE schedules SET installation = True WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()
    return

async def search_schedule_by_id(schedule_id):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schedules WHERE id = ? AND installation = False', (schedule_id,))
    result = cursor.fetchall()
    conn.close()
    return result



async def clear_schedules_db():
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM schedules")
    conn.commit()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='schedules'")
    conn.commit()
    conn.close()
    return