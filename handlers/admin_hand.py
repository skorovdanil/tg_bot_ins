import os
from collections import defaultdict

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from db import admin_db

from states import Admin

from markups import admin_markups as adm_mark

from aiogram import Router


from dotenv import load_dotenv
load_dotenv()

router = Router()



#ОТКРЫТИЕ ОСНОВНОГО МЕНЮ
@router.message(Command("admin"))
async def command_start(message: Message, state: FSMContext):
    telegram_id = str(message.from_user.id)
    admins_str = os.getenv("ADMINS_ID")
    admins_id = admins_str.split(',')
    if telegram_id in admins_id:
        await state.set_state(Admin.admin_action)
        await message.answer(f"Выберите, что вам нужно", reply_markup=adm_mark.AdminMainMenu)
    else:
        await message.answer("Доступ запрещен")


#ВОЗВРАТ В ОСНОВНОЕ МЕНЮ АДМИНА
@router.callback_query(F.data == "admin_main_menu")
async def worker_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Выберите, что вам нужно", reply_markup=adm_mark.AdminMainMenu)
    await state.set_state(Admin.admin_action)

#ВОЗВРАТ В МЕНЮ РАСПИСАНИЯ ДНЯ У АДМИНА
@router.callback_query(F.data == "admin_schedules_day_menu")
async def worker_main_menu(callback: types.CallbackQuery, state: FSMContext):
        adm_mark_days = await adm_mark.db_get_schedules_day()
        await callback.message.edit_text(f"Выберите день", reply_markup=adm_mark_days)
        await state.set_state(Admin.admin_schedules_menu)


##########Меню Отчистка расписания у монтажников
#ОБРАБОТЧИК ВЫБОРА ДНЯ НЕДЕЛИ ПРИ СОЗДАНИЕ РАСПИСАНИЕ
@router.callback_query(F.data == "admin_clear_schedules")
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Admin.admin_schedules_delete_confrim)
    confrim_menu = await adm_mark.confrim_menu()
    await callback.message.edit_text(f"Уверены в данном действие", reply_markup=confrim_menu)

@router.callback_query(Admin.admin_schedules_delete_confrim)
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "confirm_yes":
        await admin_db.clear_schedules_db()
        await callback.answer(text="Очищено", show_alert=True)
        await state.set_state(Admin.admin_action)
        await callback.message.edit_text(f"Выберите, что вам нужно", reply_markup=adm_mark.AdminMainMenu)
    else:
        await state.set_state(Admin.admin_action)
        await callback.message.edit_text(f"Выберите, что вам нужно", reply_markup=adm_mark.AdminMainMenu)



#########Меню Список монтажников
#ОБРАБОТЧИК ВЫВОДЫ СПИСКА МОНТАЖНИКОВ
@router.callback_query(F.data == "admin_list_workers_menu")
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    workers = await admin_db.get_workers_list()
    if workers:
        worker_info = []
        for worker in workers:
            worker_id = worker[0]
            name = worker[1]
            region = worker[2]
            tel_number = worker[3]
            worker_info.append(f"Имя (id): {name} ({worker_id})")
            worker_info.append(f"Регион: {region}")
            worker_info.append(f"Телефон: {tel_number}")
            worker_info.append('')

        all_workers_info = '\n'.join(worker_info).strip()

        await callback.message.edit_text(text=all_workers_info,reply_markup=adm_mark.BackMainMenu)
        await state.clear()
    else:
        await callback.message.edit_text(text="Монтажников еще нет",reply_markup=adm_mark.BackMainMenu)




##########Меню Расписание монтажников
#ОБРАБОТЧИК ВЫБОРА ДНЯ НЕДЕЛИ ПРИ СОЗДАНИЕ РАСПИСАНИЕ
@router.callback_query(F.data == "admin_schedules_menu")
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    adm_mark_days = await adm_mark.db_get_schedules_day()
    await callback.message.edit_text(f"Выберите день",reply_markup=adm_mark_days)
    await state.set_state(Admin.admin_schedules_menu)


#ОБРАБОТЧИК ВЫБОРА ВРЕМЕНИ ПРИ ИЗМЕНЕНИЕ РАСПИСАНИЯ
@router.callback_query(Admin.admin_schedules_menu)
async def worker_update_schedules(callback: types.CallbackQuery, state: FSMContext):
    day = callback.data
    await state.update_data(day=day)
    if day in await admin_db.get_schedules_day():
        work_mark_times = await adm_mark.db_get_schedules(day)
        schedules_info = work_mark_times[1][1]
        grouped = defaultdict(lambda: defaultdict(list))
        for item in schedules_info:
            worker_id = item[6]
            user = item[4]
            value = item[5]
            time = item[2]
            installation = item[7]  # 0 либо 1

            # Используем worker_id для вложенных структур
            grouped[(user, worker_id)][value].append((time, installation))


        text = f"{day}\n\n"
        for (user, worker_id), values in grouped.items():
            for value, times in values.items():
                text += f"({worker_id}) {user} {value}\n"
                for time, installation in times:
                    if installation == 1:
                        text += f"{time} - Заявка\n"
                    else:
                        text += f"{time}\n"
                text += "\n"  # Пустая строка между группами времени для одного значения

        # Удаление лишних символов новой строки в конце
        text = text.strip()

        await callback.message.edit_text(f"Выберите монтажника, которому хотите отдать заявку \n\n{text}", reply_markup=work_mark_times[0])
        await state.set_state(Admin.admin_schedules_action_confrim)



#ПОДТВЕРЖДЕНИЕ ВЫБОРА ВРЕМЕНИ У МОНТАЖНИКА
@router.callback_query(Admin.admin_schedules_action_confrim)
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(schedule_id=callback.data)
    data = await state.get_data()
    schedule_id = data.get("schedule_id")
    if await admin_db.search_schedule_by_id(schedule_id):
        confrim_menu = await adm_mark.confrim_menu()
        await callback.message.edit_text(f"Уверены в данном действие", reply_markup=confrim_menu)
        await state.set_state(Admin.admin_schedules_action)


#ОБРАБОТЧИК ВЫБОРА МОНТАЖНИКА И ИЗМЕНЕНИЕ ЕГО РАСПИСАНИЯ
@router.callback_query(Admin.admin_schedules_action)
async def worker_add_schedules(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    day = data.get("day")
    schedule_id = data.get("schedule_id")
    if callback.data == "confirm_yes":
        if await admin_db.search_schedule_by_id(schedule_id):
            await admin_db.reservation_schedule_installation(schedule_id)
            await callback.answer(text="Успешно забронированно", show_alert=True)
            work_mark_times = await adm_mark.db_get_schedules(day)
            schedules_info = work_mark_times[1][1]
            grouped = defaultdict(lambda: defaultdict(list))
            for item in schedules_info:
                worker_id = item[6]
                user = item[4]
                value = item[5]
                time = item[2]
                installation = item[7]  # 0 либо 1

                # Используем worker_id для вложенных структур
                grouped[(user, worker_id)][value].append((time, installation))

            text = f"{day}\n\n"
            for (user, worker_id), values in grouped.items():
                for value, times in values.items():
                    text += f"({worker_id}) {user} {value}\n"
                    for time, installation in times:
                        if installation == 1:
                            text += f"{time} - Заявка\n"
                        else:
                            text += f"{time}\n"
                    text += "\n"  # Пустая строка между группами времени для одного значения

            # Удаление лишних символов новой строки в конце
            text = text.strip()

            await callback.message.edit_text(f"Выберите монтажника, которому хотите отдать заявку \n\n{text}", reply_markup=work_mark_times[0])
            await state.set_state(Admin.admin_schedules_action_confrim)
    else:
        work_mark_times = await adm_mark.db_get_schedules(day)
        schedules_info = work_mark_times[1][1]
        grouped = defaultdict(lambda: defaultdict(list))
        for item in schedules_info:
            worker_id = item[6]
            user = item[4]
            value = item[5]
            time = item[2]
            installation = item[7]  # 0 либо 1

            # Используем worker_id для вложенных структур
            grouped[(user, worker_id)][value].append((time, installation))

        text = f"{day}\n\n"
        for (user, worker_id), values in grouped.items():
            for value, times in values.items():
                text += f"({worker_id}) {user} {value}\n"
                for time, installation in times:
                    if installation == 1:
                        text += f"{time} - Заявка\n"
                    else:
                        text += f"{time}\n"
                text += "\n"  # Пустая строка между группами времени для одного значения

        # Удаление лишних символов новой строки в конце
        text = text.strip()
        await callback.message.edit_text(f"Выберите монтажника, которому хотите отдать заявку \n\n{text}",reply_markup=work_mark_times[0])
        await state.set_state(Admin.admin_schedules_action_confrim)
