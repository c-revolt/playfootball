from aiogram import Bot
from aiogram.types import Message

import os

from keyboards.register_kb import register_keyboard
from utils.database import Database
from keyboards.profile_kb import profile_kb


async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Здравствуйте {users[1]}!', reply_markup=profile_kb())
    else:
        await bot.send_message(message.from_user.id,
                               text=f'😎 Привет! Очень очень рад тебя видеть!\n'
                                    f'⚽️ Помогу тебе записаться на игру по футболу в нашем городе.\n\n'
                                    f'📈 А ещё ты сможешь тут отслеживать свою статистику!\n\n\n',
                               reply_markup=register_keyboard())
