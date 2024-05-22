from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove , WebAppInfo , WebAppData
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder, KeyboardBuilder
import asyncio
from db import worker_db

# async def db_region():
#     regions = ["Краснодар", "Ростов", "Калиниград"]
#     RegionsMenu = KeyboardBuilder(button_type=InlineKeyboardButton)
#     for region in regions:
#         RegionsMenu.button(text=f"{region}")
#     RegionsMenu.adjust(2)
#     return RegionsMenu

# РАБОЧИЙ ВАРИАНТ С РЕГИОНАМИ
# async def db_region():
#     regions = await worker_db.regions()
#     EndBuyApartment = []
#     for region in regions:
#         print(region)
#         id, name = region
#         builder = []
#         builder.append(InlineKeyboardButton(text=f"{id}. {name}",callback_data=f"{id}"))
#         EndBuyApartment.append(builder)
#     print(EndBuyApartment)
#     EndBuyApartment = InlineKeyboardMarkup(inline_keyboard=EndBuyApartment)
#     return EndBuyApartment


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
    EndBuyApartment.append([InlineKeyboardButton(text="⬅ Назад", callback_data="worker_menu_out_photo")])
    EndBuyApartment = InlineKeyboardMarkup(inline_keyboard=EndBuyApartment)
    return EndBuyApartment





#МЕНЮ ОБНОВЛЕНИЯ РАСПИСАНИЯ У СОТРУДНИКА
########################################
########################################
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
    DaysUpdateSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="main_worker_menu")])
    DaysUpdateSchedules = InlineKeyboardMarkup(inline_keyboard=DaysUpdateSchedules)
    return DaysUpdateSchedules


async def db_update_schedules_time_of_day(telegram_id,day):
    times = await worker_db.get_schedules_time_of_day(telegram_id,day)

    TimesUpdateSchedules = []

    for time in times:
        MenuTimes = []
        MenuTimes.append(InlineKeyboardButton(text=f"{time}", callback_data=f"{time}"))
        TimesUpdateSchedules.append(MenuTimes)

    TimesUpdateSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="update_shulder_worker_menu")])
    TimesUpdateSchedules = InlineKeyboardMarkup(inline_keyboard=TimesUpdateSchedules)
    return TimesUpdateSchedules
################################
################################
################################



WorkerMainMenu =[
[InlineKeyboardButton(text="Составить расписание на неделю (Добавить)", callback_data="add_schedule")],
[InlineKeyboardButton(text="Изменить расписание на неделю (Удалить)", callback_data="update_schedule")],
[InlineKeyboardButton(text="Сменить район работы", callback_data="update_region")]]
WorkerMainMenu = InlineKeyboardMarkup(inline_keyboard=WorkerMainMenu)


WorkerSchedulesDaysMenu = [
[InlineKeyboardButton(text="Понедельник", callback_data="Понедельник"),
InlineKeyboardButton(text="Вторник", callback_data="Вторник")],
[InlineKeyboardButton(text="Среда", callback_data="Среда"),
InlineKeyboardButton(text="Четверг", callback_data="Четверг")],
[InlineKeyboardButton(text="Пятница", callback_data="Пятница"),
InlineKeyboardButton(text="Суббота", callback_data="Суббота")],
[InlineKeyboardButton(text="Восресенье", callback_data="Восресенье")],
[InlineKeyboardButton(text="⬅ Назад", callback_data="main_worker_menu")]
]
WorkerSchedulesDaysMenu = InlineKeyboardMarkup(inline_keyboard=WorkerSchedulesDaysMenu)


Days_Schedules = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Восресенье"]


Times_schedules = ["9:00 - 10:00", "13:00 - 14:00", "17:00 - 18:00"]

AddTimeSchedules = []
for time in Times_schedules:
    times = []
    times.append(InlineKeyboardButton(text=f"{time}", callback_data=f"{time}"))
    AddTimeSchedules.append(times)
    builder = []
AddTimeSchedules.append([InlineKeyboardButton(text="⬅ Назад", callback_data="shulder_worker_menu")])
AddTimeSchedules = InlineKeyboardMarkup(inline_keyboard=AddTimeSchedules)

