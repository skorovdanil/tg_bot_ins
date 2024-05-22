from aiogram import types, F, Router, flags, enums, Bot
from aiogram.filters import Command , CommandStart , CommandObject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove, Message, CallbackQuery, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.deep_linking import create_start_link, decode_payload


import os
import re

from states import Gen


import markups as nav


from db import worker_db



router = Router()

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    #ЕСЛИ РАБОЧИЙ УЖЕ ЗАРЕГЕСТРИРОВАН
    if await worker_db.find_worker(telegram_id) == True:
        await message.answer(f"Выберите, что вам нужно", reply_markup=nav.WorkerMainMenu)
        await state.set_state(Gen.worker_action)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Gen.registr_number)
        await message.answer("Введите ваш номер телефона")


#ИМЯ ПРИ РЕГИСТРАЦИИ
@router.message(Gen.registr_number)
async def registr_number(message: Message, state: FSMContext):
    reg_number = message.text
    pattern = re.compile(r"^(8|\+7)?\s?(9\d{2})\d{7}$")
    if re.match(pattern, reg_number):
        await state.set_state(Gen.registr_name)
        await state.update_data(number=reg_number)
        await state.update_data(telegram_id=message.from_user.id)
        await message.answer("Введите ваше имя")
    else:
        await state.set_state(Gen.registr_number)
        await message.answer("Номер телефона введен неверно, попробуйте еще раз")



#ВЫБОР РЕГИОНА ПРИ РЕГИСТАРЦИИ
@router.message(Gen.registr_name)
async def registr_name(message: Message, state: FSMContext):
    reg_name = message.text
    if len(reg_name) > 2:
        await state.set_state(Gen.registr_region)
        await state.update_data(name=message.text)
        regions = await nav.db_region()
        await message.answer_photo(photo="https://sun9-14.userapi.com/impg/IssyepRA_sRxWEgxWWqCgKjie5r9s_f-hOlbcw/G4TSsYRhlcs.jpg?size=1280x1152&quality=95&sign=f4ef9b29c9c850528f0fafb17b790c58&type=album",
                                   caption="Выберите район работы", reply_markup=regions)
    else:
        await state.set_state(Gen.registr_name)
        await message.answer("Слишком короткое имя")


#ОТКРЫТИЕ ГЛАВНОГО МЕНЮ, ПОСЛЕ УСПЕШНОЙ РЕГИСТАРЦИИ
@router.callback_query(Gen.registr_region)
async def registr_region(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    data = await state.get_data()
    number = data.get("number")
    name = data.get("name")
    region = data.get("region")
    telegram_id = data.get("telegram_id")
    await worker_db.add_worker(name,number,region,telegram_id)
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно",reply_markup=nav.WorkerMainMenu)
    await state.set_state(Gen.worker_action)




# # ОБРАБОТЧИК ГЛАВНОГО МЕНЮ У РАБОЧИХ
# @router.callback_query(Gen.worker_action)
# async def worker_action(callback: types.CallbackQuery, state: FSMContext):
#
#     if callback.data == "add_schedule":
#         data = await state.get_data()
#         await callback.message.delete()
#         await callback.message.answer(f"Выберите день",reply_markup=nav.WorkerSchedulesDaysMenu)
#         await state.set_state(Gen.worker_add_schedules)
#
#     if callback.data == "update_schedule":
#         data = await state.get_data()
#         await callback.message.delete()
#         await callback.message.answer(f"Выберите день",reply_markup=nav.WorkerSchedulesDaysMenu)
#         await state.set_state(Gen.worker_update_schedules)
#
#     if callback.data == "update_region":
#         await callback.message.delete()
#         regions = await nav.db_region()
#         await callback.message.answer_photo(
#             photo="https://sun9-14.userapi.com/impg/IssyepRA_sRxWEgxWWqCgKjie5r9s_f-hOlbcw/G4TSsYRhlcs.jpg?size=1280x1152&quality=95&sign=f4ef9b29c9c850528f0fafb17b790c58&type=album",
#             caption="Выберите район работы", reply_markup=regions)
#         await state.set_state(Gen.worker_update_region)



#ВОЗВРАТ В ОСНОВНОЕ МЕНЮ РАБОЧЕГО
@router.callback_query(F.data == "main_worker_menu")
async def add_schedule(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно", reply_markup=nav.WorkerMainMenu)
    await state.set_state(Gen.worker_action)
#ВОЗВРАТ В МЕНЮ ВЫБОРА ДЛЯ НЕДЕЛИ
@router.callback_query(F.data == "shulder_worker_menu")
async def add_schedule(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "shulder_worker_menu":
        await callback.message.delete()
        await callback.message.answer(f"Выберите день", reply_markup=nav.WorkerSchedulesDaysMenu)
        await state.set_state(Gen.worker_add_schedules)





#ОБРАБОТЧИК ВЫБОРА ДНЯ НЕДЕЛИ ПРИ СОЗДАНИЕ РАСПИСАНИЕ
@router.callback_query(F.data == "add_schedule")
async def add_schedule(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Выберите день",reply_markup=nav.WorkerSchedulesDaysMenu)
    await state.set_state(Gen.worker_add_schedules)


#ОБРАБОТЧИК ВЫБОРА ВРЕМЕНИ ПРИ СОЗДАНИЕ РАСПИСАНИЯ
@router.callback_query(Gen.worker_add_schedules)
async def registr_region(callback: types.CallbackQuery, state: FSMContext):
    if callback.data in nav.Days_Schedules:
        await state.update_data(day=callback.data)
        await callback.message.delete()
        await callback.message.answer(f"Выберите время, в которое вы свободны",reply_markup=nav.AddTimeSchedules)
        await state.set_state(Gen.worker_add_time_schedules)


#ЗАПИСЫВАНИЕ ВРЕМЕНИ В БАЗУ ДАННЫХ
@router.callback_query(Gen.worker_add_time_schedules)
async def registr_region(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = data.get("day")
    time = callback.data
    user_id = callback.from_user.id
    if day in nav.Days_Schedules:
        if time in nav.Times_schedules:
            await worker_db.add_schedules(user_id,time,day)
            await state.set_state(Gen.worker_add_time_schedules)



#ОБРАБОТЧИК ВЫБОРА ДНЯ НЕДЕЛИ ПРИ ИЗМЕНЕНИЕ РАСПИСАНИЕ
@router.callback_query(F.data == "add_schedule")
async def add_schedule(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Выберите день",reply_markup=nav.WorkerSchedulesDaysMenu)
    await state.set_state(Gen.worker_add_schedules)


#ОБРАБОТЧИК ВЫБОРА ВРЕМЕНИ ПРИ ИЗМЕНЕНИЕ РАСПИСАНИЯ
@router.callback_query(Gen.worker_update_schedules)
async def registr_region(callback: types.CallbackQuery, state: FSMContext):
    if callback.data in nav.Days_Schedules:
        await state.update_data(day=callback.data)
        await callback.message.delete()
        await callback.message.answer(f"Выберите время, в которое вы свободны",reply_markup=nav.AddTimeSchedules)
        await state.set_state(Gen.worker_add_time_schedules)


#ЗАПИСЫВАНИЕ ИЗМЕНЕННОГО ВРЕМЕНИ В БАЗУ ДАННЫХ
@router.callback_query(Gen.worker_update_time_schedules)
async def registr_region(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = data.get("day")
    time = callback.data
    user_id = callback.from_user.id
    if day in nav.Days_Schedules:
        if time in nav.Times_schedules:
            await worker_db.add_schedules(user_id,time,day)
            await state.set_state(Gen.worker_add_time_schedules)













#ОБРАБОТЧИК ВЫБОРА РЕГИОНА ДЛЯ ОБНОВЛЕНИЕ
@router.callback_query(F.data == "update_region")
async def add_schedule(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    regions = await nav.db_region()
    await callback.message.answer_photo(
        photo="https://sun9-14.userapi.com/impg/IssyepRA_sRxWEgxWWqCgKjie5r9s_f-hOlbcw/G4TSsYRhlcs.jpg?size=1280x1152&quality=95&sign=f4ef9b29c9c850528f0fafb17b790c58&type=album",
        caption="Выберите район работы", reply_markup=regions)
    await state.set_state(Gen.worker_update_region)

#ОБНОВЛЕНИЕ РЕГИОНА У РАБОЧЕГО
@router.callback_query(Gen.worker_update_region)
async def worker_update_region(callback: types.CallbackQuery, state: FSMContext):
    region = callback.data
    telegram_id = callback.from_user.id
    await worker_db.update_region(region,telegram_id)
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно",reply_markup=nav.WorkerMainMenu)
    await state.set_state(Gen.worker_action)





#ЕСЛИ НЕ НАШЕЛСЯ ОБРАБОТЧИК МЕНЮ
@router.callback_query(lambda c: True)
async def process_callback_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно", reply_markup=nav.WorkerMainMenu)
    await state.set_state(Gen.worker_action)










