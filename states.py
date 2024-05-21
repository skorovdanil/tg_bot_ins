from aiogram.fsm.state import StatesGroup, State


class Gen(StatesGroup):
    registr_number=State()
    registr_name = State()
    registr_region = State()