from aiogram.types import BotCommand, BotCommandScopeDefault
from loader import bot


async def set_commands():
    """ Установка комманд"""
    commands = [
        BotCommand(
            command='start',
            description='Регистрация'
        ),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
