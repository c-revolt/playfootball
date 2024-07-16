import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from state.create import CreateState
from keyboards.create_kb import place_kb, date_kb, time_kb
from utils.database import Database


async def create_game(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберите площадку, где будет проводиться игра.',
                           reply_markup=place_kb())
    await state.set_state(CreateState.place)


async def select_place(call_back: CallbackQuery, state: FSMContext):
    await call_back.message.answer(f'Место игры выбрано! \n'
                                   f'Дальше выбери дату.', reply_markup=date_kb())
    await state.update_data(place=call_back.data)
    await call_back.message.edit_reply_markup(reply_markup=None)
    await call_back.answer()
    await state.set_state(CreateState.date)


async def select_date(call_back: CallbackQuery, state: FSMContext):
    await call_back.message.answer(f"Я успешно сохранил дату игры \n"
                                   f"Выбери время игры", reply_markup=time_kb())
    await state.update_data(date=call_back.data)
    await call_back.message.edit_reply_markup(reply_markup=None)
    await call_back.answer()
    await state.set_state(CreateState.time)


async def select_time(call_back: CallbackQuery, state: FSMContext):
    await call_back.message.answer(f'Укажите минимальное количество игроков от 4 до 16.')
    await state.update_data(time=call_back.data)
    await call_back.message.edit_reply_markup(reply_markup=None)
    await call_back.answer()
    await state.set_state(CreateState.minplayer)


async def select_minplayer(message: Message, state: FSMContext, bot: Bot):
    if (message.text.isdigit() and 4 <= int(message.text) <= 16):
        await bot.send_message(message.from_user.id, f'Хорошо, теперь укажите максимальное число игроков. '
                                                     f'Значение должно быть от 4 до 16.')
        await state.update_data(minplayer=message.text)
        await state.set_state(CreateState.maxplayer)
    else:
        await bot.send_message(message.from_user.id, text="Так, что-то не то. Попробуй ещё раз?")


async def select_maxplayer(message: Message, state: FSMContext, bot: Bot):
    if (message.text.isdigit() and 4 <= int(message.text) <= 16):
        await bot.send_message(message.from_user.id, text='Теперь нужно указать стоимость игры.')
        await state.update_data(maxplayer=message.text)
        await state.set_state(CreateState.price)
    else:
        await bot.send_message(message.from_user.id, text="Так, что-то не то со стоимостью. Попробуй ещё раз?")


async def select_price(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, text='Готово! Я записал тебя на игру!')
    await state.update_data(price=message.text)
    create_data = await state.get_data()
    create_time = create_data.get('time').split('_')[1]
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_game(
        create_data['place'],
        create_data['date'],
        create_time,
        create_data['minplayer'],
        create_data['maxplayer'],
        create_data['price']
    )
    await state.clear()

