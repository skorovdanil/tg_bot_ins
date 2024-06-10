from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove , WebAppInfo , WebAppData
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder, KeyboardBuilder
import asyncio

from db import admin_db
#from db import main_db


#КНОПКА ВОЗРВАТА В ГЛАВНОЕ МЕНЮ АДМИНА
BackMainMenu = [
[InlineKeyboardButton(text="⬅ Назад", callback_data="admin_main_menu")]
]
BackMainMenu = InlineKeyboardMarkup(inline_keyboard=BackMainMenu)


async def db_get_schedules_day():
    days = await admin_db.get_schedules_day()
    DaysUpdateSchedules = []
    MenuDays = []
    for day in days:
        MenuDays.append(InlineKeyboardButton(text=f"{day}", callback_data=f"{day}"))

        if len(MenuDays) == 2:
            DaysUpdateSchedules.append(MenuDays)
            MenuDays = []

    if MenuDays:
        DaysUpdateSchedules.append(MenuDays)
    DaysUpdateSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="admin_main_menu")])
    DaysUpdateSchedules = InlineKeyboardMarkup(inline_keyboard=DaysUpdateSchedules)
    return DaysUpdateSchedules

async def db_get_schedules(day):
    shedules_info = await admin_db.get_schedules_worker_info(day)
    if shedules_info:
        SchedulesAdminMenu = []
        for item in shedules_info[0]:
            MenuTimes = []
            MenuTimes.append(InlineKeyboardButton(text=f"({item[6]}) {item[4]} {item[5]} {item[2]}", callback_data=f"{item[1]}"))
            SchedulesAdminMenu.append(MenuTimes)

        SchedulesAdminMenu.append([InlineKeyboardButton(text="⬅ Назад", callback_data="admin_schedules_day_menu")])
        SchedulesAdminMenu = InlineKeyboardMarkup(inline_keyboard=SchedulesAdminMenu)
        return SchedulesAdminMenu, shedules_info

async def confrim_menu():
    ConfrimMenu = []
    ConfrimMenu.append([InlineKeyboardButton(text="Да", callback_data="confirm_yes")])
    ConfrimMenu.append([InlineKeyboardButton(text="Отменить", callback_data="confirm_no")])
    ConfrimMenu = InlineKeyboardMarkup(inline_keyboard=ConfrimMenu)
    return ConfrimMenu

#ГЛАВНОЕ МЕНЮ АДМИНА
AdminMainMenu =[
[InlineKeyboardButton(text="Список монтажников", callback_data="admin_list_workers_menu")],
[InlineKeyboardButton(text="Расписание монтажников", callback_data="admin_schedules_menu")],
[InlineKeyboardButton(text="Отчистка расписания у всех монтажников (делать раз в неделю)", callback_data="admin_clear_schedules")]]
AdminMainMenu = InlineKeyboardMarkup(inline_keyboard=AdminMainMenu)



#МЕНЮ С ДНЯМИ НЕДЕЛИ
AdminSchedulesDaysMenu = [
[InlineKeyboardButton(text="Понедельник", callback_data="Понедельник"),
InlineKeyboardButton(text="Вторник", callback_data="Вторник")],
[InlineKeyboardButton(text="Среда", callback_data="Среда"),
InlineKeyboardButton(text="Четверг", callback_data="Четверг")],
[InlineKeyboardButton(text="Пятница", callback_data="Пятница"),
InlineKeyboardButton(text="Суббота", callback_data="Суббота")],
[InlineKeyboardButton(text="Воскресенье", callback_data="Воскресенье")],
[InlineKeyboardButton(text="⬅ Назад", callback_data="admin_main_menu")]
]
AdminSchedulesDaysMenu = InlineKeyboardMarkup(inline_keyboard=AdminSchedulesDaysMenu)

#СПИОСОК ДНЕЙ НЕДЕЛИ
Days_Schedules = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]

#СПИСОК ДОСТУПНЫХ ВРЕМЕННЫХ ДИАПАЗОНОВ
Times_schedules = ["9:00 - 10:00", "13:00 - 14:00", "17:00 - 18:00"]