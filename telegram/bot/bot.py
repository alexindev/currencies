from loader import dp, bot
from bot.handlers.settings import settings_handlers
from bot.handlers.user import user_handlers
from bot.keyboars.commands import set_commands


async def start_bot():
    """Запуск бота"""
    await set_commands()
    user_handlers(dp)
    settings_handlers(dp)

    try:
        print('Bot started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
