import sqlite3

async def find_worker(telegram_id):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM worker WHERE telegram_id = ?', (telegram_id,))
    find_userid = cursor.fetchone()
    conn.close()
    if find_userid:
        return True
    else:
        return False


async def add_worker(name,number,region,telegram_id):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO worker(name,tel_number,region,telegram_id,date)'
                   'VALUES (?,?,?,?,datetime("now", "+3 hours"))',
                   (name,number,region,telegram_id))
    conn.commit()
    conn.close()
    return

async def update_region(region, telegram_id):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE worker SET region = ? WHERE telegram_id = ?', (region, telegram_id))
    conn.commit()
    conn.close()
    return



async def add_schedules(telegram_id,time,day):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM schedules WHERE worker_id = ? AND time = ? AND day = ?', (telegram_id,time,day))
    result = cursor.fetchone()
    if result:
        conn.close()
        return False
    else:
        cursor.execute('INSERT INTO schedules(worker_id,time,day,date) VALUES (?,?,?,datetime("now", "+3 hours"))', (telegram_id, time, day))
        conn.commit()
        conn.close()
        return True




async def get_schedules_day(telegram_id):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT day FROM schedules WHERE worker_id = ?', (telegram_id,))
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

async def get_schedules_time_of_day(telegram_id,day):
    conn = sqlite3.connect('db/installation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT time FROM schedules WHERE worker_id = ? AND day = ?', (telegram_id, day))
    result = cursor.fetchall()
    conn.close()
    values = [item[0] for item in result]
    return values