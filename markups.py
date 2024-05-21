from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove , WebAppInfo , WebAppData
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder, KeyboardBuilder
import json
import asyncio

# async def db_region():
#     regions = ["Краснодар", "Ростов", "Калиниград"]
#     RegionsMenu = KeyboardBuilder(button_type=InlineKeyboardButton)
#     for region in regions:
#         RegionsMenu.button(text=f"{region}")
#     RegionsMenu.adjust(2)
#     return RegionsMenu

#
async def db_region():
    regions = [{0:"Краснодар"},
               {1:"Ростов"},
               {0: "Калининград"}
               ]
    EndBuyApartment = []
    for region in regions:
        for id, name in region.items():
            builder = []
            builder.append(InlineKeyboardButton(text=f"{name}",callback_data=f"region{id}"))
            EndBuyApartment.append(builder)
    print(EndBuyApartment)
    EndBuyApartment = InlineKeyboardMarkup(inline_keyboard=EndBuyApartment)
    return EndBuyApartment






