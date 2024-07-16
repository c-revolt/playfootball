from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Перезапуск бота"),
        BotCommand(command="help", description="Помощь по этому боту")
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
