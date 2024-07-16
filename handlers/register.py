from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import re
import os

from utils.database import Database
from state.register import RegisterState
from keyboards.profile_kb import profile_kb


async def start_register(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if(users):
        await bot.send_message(message.from_user.id,
                               f'{users[1]} \nВы уже заригистрированы.', reply_markup=profile_kb)
    else:
        await bot.send_message(message.from_user.id,
                               text='Ок, давай начнём регистрацию. Для начала скажи, как я могу к тебе обращаться?')
        await state.set_state(RegisterState.regName)


async def register_name(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id,text=f'☺️ О, приятно познакомиться {message.text}!\n'
                              f'Чтобы оставаться на связи, укажи, пожалуйста свой номер телефона.\n'
                              f'📲 Формат телефона: +7xxxxxxxxxx\n\n'
                              f'⚠️ Вводи осторожно! Я очень чувствительный к формату ⚠️')
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)


async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if (re.findall(r'^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message.text)):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('regname')
        reg_phone = reg_data.get('regphone')
        msg = (f'🪪 Что ж, приятно познакомиться {reg_name}.\n'
               f'📲 Твой телефон: {reg_phone}')
        await bot.send_message(message.from_user.id, msg)
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_user(reg_name, reg_phone, message.from_user.id)
        await state.clear()

    else:
        await bot.send_message(message.from_user.id,
                               text='🫢 Ой, похоже что номер указан в не правильном формате.\n'
                                  '🥺 Попробуй ещё раз, пожалуйста.')
