import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command

from dotenv import load_dotenv

from utils.commands import set_commands
from state.register import RegisterState
from state.create import CreateState
from handlers.start import get_start
from handlers.profile import viewn_games, viewn_game_date
from handlers.register import start_register, register_name, register_phone
from handlers.admin.create import create_game, select_place, select_date, select_time, select_minplayer, \
    select_maxplayer, select_price
from filters.CheckAdmin import CheckAdmin

load_dotenv()

token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def start_bot(bot: Bot):
    await bot.send_message(461589641, text="Бот запущен!")


dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

# Регистрируем хендлеры этапов регистрации
dp.message.register(start_register, F.text == '🪪 Зарегистрироваться')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)
# Регистрируем хендлеры для создания игры
dp.message.register(create_game, Command(commands='create'), CheckAdmin())
dp.callback_query.register(select_place, CreateState.place)
dp.callback_query.register(select_date, CreateState.date)
dp.callback_query.register(select_time, CreateState.time)
dp.message.register(select_minplayer, CreateState.minplayer)
dp.message.register(select_maxplayer, CreateState.maxplayer)
dp.message.register(select_price, CreateState.price)
# Регистрируем хендлеры профиля
dp.message.register(viewn_games, F.text == "Актуальные игры")
dp.callback_query.register(viewn_game_date, F.data.starswith('viewn_date_'))


async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    except:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
