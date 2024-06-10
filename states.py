from aiogram.fsm.state import StatesGroup, State


class Worker(StatesGroup):
    registr_number = State()
    registr_name = State()
    registr_region = State()


    worker_action = State()

    worker_add_schedules = State()
    worker_add_time_schedules = State()

    worker_update_schedules = State()
    worker_update_time_schedules = State()
    worker_update_time_schedules_confrim = State()

    worker_update_region = State()


class Admin(StatesGroup):

    admin_action = State()
    admin_schedules_menu = State()
    admin_schedules_action = State()

    admin_schedules_action_confrim = State()
    admin_schedules_delete_confrim = State()