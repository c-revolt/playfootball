import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from utils.database import Database
from utils.function import list_gamer
from keyboards.profile_kb import date_kb, add_match, delete_match


async def viewn_games(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text=f'Выберите дату игры.', reply_markup=date_kb())


async def viewn_game_date(callback: CallbackQuery):
    await callback.answer()
    date = callback.data.split("_")[-1]
    db = Database(os.getenv('DATABASE_NAME'))
    games = db.select_games('0', date)
    if (games):
        await callback.message.answer(f'Актуальные игры:')
        for game in games:
            players = db.select_players(game[0])
            gamers = list_gamer(players)
            msg = (f'Игра состоится: {game[9]} (Адрес: {game[10]}) \n'
                   f' {game[2]} в {game[3]} \n'
                   f'Количество участников от {game[4]} до {game[5]} \n'
                   f'Стоимость игры {game[6]} \n'
                   f'{gamers}')
            if not (db.check_user(game[0], callback.from_user.id)):
                await callback.message.answer(msg, reply_markup=add_match(game[0], callback.from_user.id))
            else:
                await callback.message.answer(msg, reply_markup=delete_match(game[0], callback.from_user.id))
    else:
        await callback.message.answer(f'В выбранную дату игр нет.')

# async def view_profile(message: Message, bot: Bot):
#     db = Database(os.getenv('DATABASE_NAME'))
#     games = db.db_select_column('games', 'status', 0)
#     if(games):
#         await bot.send_message(message.from_user.id, f'Актуальные игры:')
#         for game in games:
#             await bot.send_message(message.from_user.id,
#                                    text=f'Игра состоится: {game[2]}, {game[3]} \n'
#                                         f'Минимальное число участников: {game[4]} \n'
#                                         f'Максимальное число участников: {game[5]} \n'
#                                         f'Стоимость игры: {game[6]}')
#     else:
#         await bot.send_message(message.from_user.id, f'В настоящее время игр пока не планируется.')
