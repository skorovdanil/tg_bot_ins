from aiogram import types, F, Router, flags, enums, Bot
from aiogram.filters import Command , CommandStart , CommandObject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.deep_linking import create_start_link, decode_payload

import re

from states import Gen


import markups as nav


#from db import users_db



router = Router()

@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    await state.set_state(Gen.registr_number)
    await message.answer("Введите ваш номер")
    print(message.from_user.id)


@router.message(Gen.registr_number)
async def command_start(message: Message, state: FSMContext):
    reg_number = message.text
    pattern = re.compile(r"^(8|\+7)?\s?(9\d{2})\d{7}$")
    if re.match(pattern, reg_number):
        await state.set_state(Gen.registr_name)
        await state.update_data(number=reg_number)
        await message.answer("Введите ваше имя")
    else:
        await state.set_state(Gen.registr_number)
        await message.answer("Номер телефона введен неверно, попробуйте еще раз")


@router.message(Gen.registr_name)
async def command_start(message: Message, state: FSMContext):
    reg_name = message.text
    if len(reg_name) > 2:
        await state.set_state(Gen.registr_region)
        await state.update_data(name=message.text)
        regions = await nav.db_region()
        await message.answer("Выберите ваш регион",reply_markup=regions)
    else:
        await state.set_state(Gen.registr_name)
        await message.answer("Слишком короткое имя")

@router.message(Gen.registr_region)
async def command_start(message: Message, state: FSMContext, callback_query: CallbackQuery):
    reg_name = message.text
    if len(reg_name) > 2:
        await state.set_state(Gen.registr_region)
        await state.update_data(name=message.text)
        regions = await nav.db_region()
        await message.answer("Выберите ваш регион",reply_markup=regions)
    else:
        await state.set_state(Gen.registr_name)
        await message.answer("Слишком короткое имя")



