from aiogram.fsm.state import StatesGroup, State


class Gen(StatesGroup):
    registr_number = State()
    registr_name = State()
    registr_region = State()


    worker_action = State()

    worker_add_schedules = State()
    worker_add_time_schedules = State()

    worker_update_schedules = State()
    worker_update_time_schedules = State()

    worker_update_region = State()


    admin_action = State()
