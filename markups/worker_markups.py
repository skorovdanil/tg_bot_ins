from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove , WebAppInfo , WebAppData
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder, KeyboardBuilder
import asyncio
from db import worker_db

#ТАБЛИЦА РЕГИОНОВ
async def db_region():
    EndBuyApartment = []
    builder = []
    for i in range(1,17):
        builder.append(InlineKeyboardButton(text=f"{i}",callback_data=f"{i}"))

        if len(builder) == 4:
            EndBuyApartment.append(builder)
            builder = []

    if builder:
        EndBuyApartment.append(builder)
    EndBuyApartment.append([InlineKeyboardButton(text="⬅ Назад", callback_data="worker_region_main_menu")])
    EndBuyApartment = InlineKeyboardMarkup(inline_keyboard=EndBuyApartment)
    return EndBuyApartment

#КНОПКА ВОЗРВАТА В ГЛАВНОЕ МЕНЮ
BackMainMenu = [
[InlineKeyboardButton(text="⬅ Назад", callback_data="worker_main_menu")]
]
BackMainMenu = InlineKeyboardMarkup(inline_keyboard=BackMainMenu)


#МЕНЮ ОБНОВЛЕНИЯ РАСПИСАНИЯ У СОТРУДНИКА
########################################
########################################
#ВЫБОР ДНЯ НЕДЕЛИ
async def db_update_schedules_day(telegram_id):
    days = await worker_db.get_schedules_day(telegram_id)
    DaysUpdateSchedules = []
    MenuDays = []
    for day in days:
        MenuDays.append(InlineKeyboardButton(text=f"{day}", callback_data=f"{day}"))

        if len(MenuDays) == 2:
            DaysUpdateSchedules.append(MenuDays)
            MenuDays = []

    if MenuDays:
        DaysUpdateSchedules.append(MenuDays)
    DaysUpdateSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="worker_main_menu")])
    DaysUpdateSchedules = InlineKeyboardMarkup(inline_keyboard=DaysUpdateSchedules)
    return DaysUpdateSchedules

#ВЫБОР ВРЕМЕНИ
async def db_update_schedules_time_of_day(telegram_id,day):
    times = await worker_db.get_schedules_time_of_day(telegram_id,day)

    TimesUpdateSchedules = []

    for time in times:
        MenuTimes = []
        MenuTimes.append(InlineKeyboardButton(text=f"{time}", callback_data=f"{time}"))
        TimesUpdateSchedules.append(MenuTimes)

    TimesUpdateSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="worker_update_schedules_day_menu")])
    TimesUpdateSchedules = InlineKeyboardMarkup(inline_keyboard=TimesUpdateSchedules)
    return TimesUpdateSchedules
################################
################################
################################


#ГЛАВНОЕ МЕНЮ РАБОТНИКА
WorkerMainMenu =[
[InlineKeyboardButton(text="Составить расписание на неделю (Добавить)", callback_data="worker_add_schedules")],
[InlineKeyboardButton(text="Изменить расписание на неделю (Удалить)", callback_data="worker_update_schedules")],
[InlineKeyboardButton(text="Посмотреть моё расписание", callback_data="worker_all_schedules")],
[InlineKeyboardButton(text="Сменить район работы", callback_data="worker_update_region")]]
WorkerMainMenu = InlineKeyboardMarkup(inline_keyboard=WorkerMainMenu)


#МЕНЮ С ДНЯМИ НЕДЕЛИ
WorkerSchedulesDaysMenu = [
[InlineKeyboardButton(text="Понедельник", callback_data="Понедельник"),
InlineKeyboardButton(text="Вторник", callback_data="Вторник")],
[InlineKeyboardButton(text="Среда", callback_data="Среда"),
InlineKeyboardButton(text="Четверг", callback_data="Четверг")],
[InlineKeyboardButton(text="Пятница", callback_data="Пятница"),
InlineKeyboardButton(text="Суббота", callback_data="Суббота")],
[InlineKeyboardButton(text="Воскресенье", callback_data="Воскресенье")],
[InlineKeyboardButton(text="⬅ Назад", callback_data="worker_main_menu")]
]
WorkerSchedulesDaysMenu = InlineKeyboardMarkup(inline_keyboard=WorkerSchedulesDaysMenu)

#СПИОСОК ДНЕЙ НЕДЕЛИ
Days_Schedules = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

#СПИСОК ДОСТУПНЫХ ВРЕМЕННЫХ ДИАПАЗОНОВ
Times_schedules = ["9:00 - 10:00", "13:00 - 14:00", "17:00 - 18:00"]


#МЕНЮ С ЧАСАМИ РАБОТЫ (ДЛЯ РАСПИСАНИЯ)
AddTimeSchedules = []
for time in Times_schedules:
    times = []
    times.append(InlineKeyboardButton(text=f"{time}", callback_data=f"{time}"))
    AddTimeSchedules.append(times)
    builder = []
AddTimeSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="worker_schedules_day_menu")])
AddTimeSchedules = InlineKeyboardMarkup(inline_keyboard=AddTimeSchedules)

