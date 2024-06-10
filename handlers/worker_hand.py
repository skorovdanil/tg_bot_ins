from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv
load_dotenv()
import  os

import re
from states import Admin

from markups import admin_markups as adm_mark

from states import Worker

from markups import worker_markups as work_mark

from db import main_db


router = Router()

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    # ЕСЛИ АДМИН
    telegram_id = str(message.from_user.id)
    # admins_str = os.getenv("ADMINS_ID")
    # admins_id = admins_str.split(',')
    # if telegram_id in admins_id:
    #     await state.set_state(Admin.admin_action)
    #     await message.answer(f"Выберите, что вам нужно", reply_markup=adm_mark.AdminMainMenu)

    #ЕСЛИ РАБОЧИЙ УЖЕ ЗАРЕГЕСТРИРОВАН
    if await main_db.find_worker(telegram_id) == True:
        await message.answer(f"Выберите, что вам нужно", reply_markup=work_mark.WorkerMainMenu)
        await state.set_state(Worker.worker_action)

    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ (НЕ ЗАГЕСТРИРОВАН)
        await state.set_state(Worker.registr_number)
        await message.answer("Введите ваш номер телефона")



#ИМЯ ПРИ РЕГИСТРАЦИИ
@router.message(Worker.registr_number)
async def registr_number(message: Message, state: FSMContext):
    reg_number = message.text
    pattern = re.compile(r"^(8|\+7)?\s?(9\d{2})\d{7}$")
    if re.match(pattern, reg_number):
        await state.set_state(Worker.registr_name)
        await state.update_data(number=reg_number)
        await state.update_data(telegram_id=message.from_user.id)
        await message.answer("Введите ваше имя")
    else:
        await state.set_state(Worker.registr_number)
        await message.answer("Номер телефона введен неверно, попробуйте еще раз")



#ВЫБОР РЕГИОНА ПРИ РЕГИСТАРЦИИ
@router.message(Worker.registr_name)
async def registr_name(message: Message, state: FSMContext):
    reg_name = message.text
    if len(reg_name) > 2:
        await state.set_state(Worker.registr_region)
        await state.update_data(name=message.text)
        regions = await work_mark.db_region()
        await message.answer_photo(photo="https://sun9-14.userapi.com/impg/IssyepRA_sRxWEgxWWqCgKjie5r9s_f-hOlbcw/G4TSsYRhlcs.jpg?size=1280x1152&quality=95&sign=f4ef9b29c9c850528f0fafb17b790c58&type=album",
                                   caption="Выберите район работы", reply_markup=regions)
    else:
        await state.set_state(Worker.registr_name)
        await message.answer("Слишком короткое имя")


#ОТКРЫТИЕ ГЛАВНОГО МЕНЮ, ПОСЛЕ УСПЕШНОЙ РЕГИСТАРЦИИ
@router.callback_query(Worker.registr_region)
async def registr_region(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=callback.data)
    data = await state.get_data()
    number = data.get("number")
    name = data.get("name")
    region = data.get("region")
    telegram_id = data.get("telegram_id")
    await main_db.add_worker(name,number,region,telegram_id)
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно",reply_markup=work_mark.WorkerMainMenu)
    await state.set_state(Worker.worker_action)


#ВОЗВРАТ В ОСНОВНОЕ МЕНЮ РАБОЧЕГО
@router.callback_query(F.data == "worker_main_menu")
async def worker_main_menu(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    #ЕСЛИ РАБОЧИЙ УЖЕ ЗАРЕГЕСТРИРОВАН
    if await main_db.find_worker(telegram_id) == True:
        await callback.message.edit_text(f"Выберите, что вам нужно", reply_markup=work_mark.WorkerMainMenu)
        await state.set_state(Worker.worker_action)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")

# ВОЗВРАТ В ОСНОВНОЕ МЕНЮ РАБОЧЕГО ИЗ МЕНЮ С ФОТО
@router.callback_query(F.data == "worker_region_main_menu")
async def worker_region_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно", reply_markup=work_mark.WorkerMainMenu)
    await state.set_state(Worker.worker_action)
#ВОЗВРАТ В МЕНЮ ВЫБОРА ДНЯ НЕДЕЛИ ПРИ СОЗДАНИЕ
@router.callback_query(F.data == "worker_schedules_day_menu")
async def worker_schedules_day_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Выберите день", reply_markup=work_mark.WorkerSchedulesDaysMenu)
    await state.set_state(Worker.worker_add_schedules)


#ВОЗВРАТ В МЕНЮ ВЫБОРА ДЛЯ НЕДЕЛИ ПРИ ОБНОВЛЕНИЕ
@router.callback_query(F.data == "worker_update_schedules_day_menu")
async def worker_schedules_day_menu(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    work_mark_days = await work_mark.db_update_schedules_day(telegram_id)
    await callback.message.edit_text(f"Выберите день", reply_markup=work_mark_days)
    await state.set_state(Worker.worker_update_schedules)









#ОБРАБОТЧИК ВЫБОРА ДНЯ НЕДЕЛИ ПРИ СОЗДАНИЕ РАСПИСАНИЕ
@router.callback_query(F.data == "worker_add_schedules")
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    # ЕСЛИ РАБОЧИЙ УЖЕ ЗАРЕГЕСТРИРОВАН
    if await main_db.find_worker(telegram_id) == True:
        await callback.message.edit_text(f"Выберите день",reply_markup=work_mark.WorkerSchedulesDaysMenu)
        await state.set_state(Worker.worker_add_schedules)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")


#ОБРАБОТЧИК ВЫБОРА ВРЕМЕНИ ПРИ СОЗДАНИЕ РАСПИСАНИЯ
@router.callback_query(Worker.worker_add_schedules)
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    if callback.data in work_mark.Days_Schedules:
        await state.update_data(day=callback.data)
        await callback.message.edit_text(f"Выберите время, в которое вы свободны",reply_markup=work_mark.AddTimeSchedules)
        await state.set_state(Worker.worker_add_time_schedules)



#ЗАПИСЫВАНИЕ ВРЕМЕНИ В БАЗУ ДАННЫХ И ОТСЫЛАЕМ УВЕДОМЛЕНИЕ АДМИНАМ
@router.callback_query(Worker.worker_add_time_schedules)
async def worker_add_time_schedules(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = data.get("day")
    time = callback.data
    telegram_id = callback.from_user.id
    # ЕСЛИ РАБОЧИЙ УЖЕ ЗАРЕГЕСТРИРОВАН
    if await main_db.find_worker(telegram_id) == True:
        if day in work_mark.Days_Schedules:
            if time in work_mark.Times_schedules:
                await main_db.add_schedules(telegram_id,time,day)
                await state.set_state(Worker.worker_add_time_schedules)
                await callback.answer(text="Успешно добавлено", show_alert=True)
            elif callback.data == "all_day":
                for schedule_time in work_mark.Times_schedules:
                    await main_db.add_schedules(telegram_id, schedule_time, day)
                await callback.answer(text="Успешно добавлено", show_alert=True)
                await callback.message.edit_text(f"Выберите день", reply_markup=work_mark.WorkerSchedulesDaysMenu)
                await state.set_state(Worker.worker_add_schedules)

                # admins_str = os.getenv("ADMINS_ID")
                # admins_id = admins_str.split(',')
                # for admin in admins_id:
                #     await callback.message.bot.send_message(text=f"🕑Обновлено расписание на {day}", chat_id=admin)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")





#ОБРАБОТЧИК ВЫБОРА ДНЯ НЕДЕЛИ ПРИ ИЗМЕНЕНИЕ РАСПИСАНИЕ
@router.callback_query(F.data == "worker_update_schedules")
async def worker_update_schedules(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    if await main_db.find_worker(telegram_id) == True:
        work_mark_days = await work_mark.db_update_schedules_day(telegram_id)
        await callback.message.edit_text(f"Выберите день", reply_markup=work_mark_days)
        await state.set_state(Worker.worker_update_schedules)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")





#ОБРАБОТЧИК ВЫБОРА ВРЕМЕНИ ПРИ ИЗМЕНЕНИЕ РАСПИСАНИЯ
@router.callback_query(Worker.worker_update_schedules)
async def worker_update_schedules(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data
    telegram_id = callback.from_user.id
    if day in await main_db.get_schedules_day(callback.from_user.id):
        work_mark_times = await work_mark.db_update_schedules_time_of_day(telegram_id,day)
        await state.update_data(day=callback.data)
        await callback.message.edit_text(f"Выберите время, которые хотите удалить",reply_markup=work_mark_times)
        await state.set_state(Worker.worker_update_time_schedules_confrim)



#ОБРАБОТЧИК ПОДТВЕРЖДЕНИЯ ДЕЙСТВИЯ ПРИ ВЫБОРА ВРЕМЕНИ ПРИ ИЗМЕНЕНИЕ РАСПИСАНИЯ
@router.callback_query(Worker.worker_update_time_schedules_confrim)
async def worker_update_schedules(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(time=callback.data)
    data = await state.get_data()
    day = data.get("day")
    telegram_id = callback.from_user.id

    if await main_db.find_worker(telegram_id) == True:
        if day in await main_db.get_schedules_day(callback.from_user.id):
            confrim_menu = await work_mark.confrim_menu()
            await callback.message.edit_text(f"Уверены в данном действие", reply_markup=confrim_menu)
            await state.set_state(Worker.worker_update_time_schedules)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")


#ЗАПИСЫВАНИЕ ИЗМЕНЕННОГО ВРЕМЕНИ В БАЗУ ДАННЫХ И ОТСЫЛАЕМ УВЕДОМЛЕНИЕ АДМИНАМ
@router.callback_query(Worker.worker_update_time_schedules)
async def worker_update_time_schedules(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = data.get("day")
    time = data.get("time")
    telegram_id = callback.from_user.id
    # ЕСЛИ РАБОЧИЙ УЖЕ ЗАРЕГЕСТРИРОВАН
    if callback.data == "confirm_yes":
        if await main_db.find_worker(telegram_id) == True:
            if day in await main_db.get_schedules_day(callback.from_user.id):
                if time in await main_db.get_schedules_time_of_day(callback.from_user.id, day):
                    await main_db.delete_schedules_time(telegram_id,time,day)
                    work_mark_times = await work_mark.db_update_schedules_time_of_day(telegram_id, day)
                    await callback.answer(text="Удалено", show_alert=True)
                    await callback.message.edit_text(f"Выберите время, которые хотите удалить", reply_markup=work_mark_times)
                    await state.set_state(Worker.worker_update_time_schedules)

                    admins_str = os.getenv("ADMINS_ID")
                    admins_id = admins_str.split(',')
                    for admin in admins_id:
                        await callback.message.bot.send_message(text=f"🕑Обновлено расписание на {day}", chat_id=admin)
                else:
                    work_mark_times = await work_mark.db_update_schedules_time_of_day(telegram_id, day)
                    await callback.message.edit_text(f"Выберите время, которые хотите удалить",
                                                     reply_markup=work_mark_times)
                    await state.set_state(Worker.worker_update_time_schedules)
                    await callback.answer(text="Эти данные не акутальны", show_alert=True)
        else:
            #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
            await state.set_state(Worker.registr_number)
            await callback.message.delete()
            await callback.message.answer("Введите ваш номер телефона")
    else:
        work_mark_times = await work_mark.db_update_schedules_time_of_day(telegram_id, day)
        await callback.message.edit_text(f"Выберите время, которые хотите удалить", reply_markup=work_mark_times)
        await state.set_state(Worker.worker_update_time_schedules_confrim)





#ОБРАБОТЧИК ВЫВОДА ПОЛНОГО РАСПИСАНИЯ У СОТРУДНИКА
@router.callback_query(F.data == "worker_all_schedules")
async def worker_all_schedules(callback: types.CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    if await main_db.find_worker(telegram_id) == True:
        data = await main_db.worker_all_schedules(telegram_id)
        if data:
            final_text = ""
            for day_schedule in data:
                day = day_schedule[0]
                final_text += f"{day}\n"

                for time, installation in day_schedule[1:]:
                    if installation == 1:
                        final_text += f"{time} (Заявка)\n"
                    else:
                        final_text += f"{time}\n"

                final_text += "\n"

            await callback.message.edit_text(text=final_text, reply_markup=work_mark.BackMainMenu)
        else:
            await callback.message.edit_text(text="У вас еще нет расписания", reply_markup=work_mark.BackMainMenu)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")


#ОБРАБОТЧИК ВЫБОРА РЕГИОНА ДЛЯ ОБНОВЛЕНИЕ
@router.callback_query(F.data == "worker_update_region")
async def worker_update_region(callback: types.CallbackQuery, state: FSMContext):
    regions = await work_mark.db_region()
    telegram_id = callback.from_user.id
    if await main_db.find_worker(telegram_id) == True:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo="https://sun9-14.userapi.com/impg/IssyepRA_sRxWEgxWWqCgKjie5r9s_f-hOlbcw/G4TSsYRhlcs.jpg?size=1280x1152&quality=95&sign=f4ef9b29c9c850528f0fafb17b790c58&type=album",
            caption="Выберите район работы", reply_markup=regions)
        await state.set_state(Worker.worker_update_region)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")

#ОБНОВЛЕНИЕ РЕГИОНА У РАБОЧЕГО
@router.callback_query(Worker.worker_update_region)
async def worker_update_region(callback: types.CallbackQuery, state: FSMContext):
    region = callback.data
    telegram_id = callback.from_user.id
    await main_db.worker_update_region(region,telegram_id)
    await callback.message.delete()
    await callback.message.answer(f"Выберите, что вам нужно",reply_markup=work_mark.WorkerMainMenu)
    await state.set_state(Worker.worker_action)





#ЕСЛИ НЕ НАШЕЛСЯ ОБРАБОТЧИК МЕНЮ(по callback)
@router.callback_query(lambda c: True)
async def other_callback(callback: CallbackQuery, state: FSMContext):
    telegram_id = str(callback.from_user.id)
    admins_str = os.getenv("ADMINS_ID")
    admins_id = admins_str.split(',')
    if telegram_id in admins_id:
        await state.set_state(Admin.admin_action)
        await callback.message.delete()
        await callback.message.answer(f"Выберите, что вам нужно", reply_markup=adm_mark.AdminMainMenu)
    elif await main_db.find_worker(telegram_id) == True:
        await callback.message.delete()
        await callback.message.answer(f"Выберите, что вам нужно", reply_markup=work_mark.WorkerMainMenu)
        await state.set_state(Worker.worker_action)
    else:
        #НОМЕР ТЕЛЕФОНА ПРИ РЕГИСТРАЦИИ
        await state.set_state(Worker.registr_number)
        await callback.message.delete()
        await callback.message.answer("Введите ваш номер телефона")











