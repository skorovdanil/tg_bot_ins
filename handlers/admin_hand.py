from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.deep_linking import create_start_link, decode_payload
from dotenv import load_dotenv
load_dotenv()
import os
import re
from states import Gen
import markups as nav
from db import worker_db

router = Router()
