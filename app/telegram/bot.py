from app.telegram.loader import dp, bot
from app.telegram.handlers.settings import settings_handlers
from app.telegram.handlers.user import user_handlers
from app.telegram.keyboars.commands import set_commands


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
