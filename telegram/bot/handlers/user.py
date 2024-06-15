import ujson

from aiogram import types, Dispatcher, F

from broker import send_message_to_queue
from loader import bot, db
from bot.keyboars.inline import main_kb, back_kb


async def start_menu(message: types.Message):
    """ Стартовое сообщение """
    db.new_user(chat_id=message.from_user.id)
    await bot.send_message(message.from_user.id, text="Главное меню:", reply_markup=main_kb())


async def start_menu_cb(callback: types.CallbackQuery):
    """ Стартовое сообщение c callback"""
    await callback.answer()
    await callback.message.edit_text(text="Выберите меню:", reply_markup=main_kb())


async def start_bot(callback: types.CallbackQuery):
    """ Запустить мониторинг """
    await callback.answer()
    user_data = db.get_user(chat_id=callback.from_user.id)
    long_percent = user_data.get('long_percent')
    long_time = user_data.get('long_time')
    short_percent = user_data.get('short_percent')
    short_time = user_data.get('short_time')

    if (long_percent and long_time) or (short_percent and short_time):
        user_data['func'] = 'start'
        send_message_to_queue(message=ujson.dumps(user_data))
        await callback.message.edit_text(text='Мониторинг запущен', reply_markup=back_kb())
    else:
        await callback.message.edit_text(text='Не достаточно данных для мониторинга', reply_markup=back_kb())


async def stop_bot(callback: types.CallbackQuery):
    """ Остановить мониторинг """
    await callback.answer()
    message = {
        'func': 'stop',
        'chat_id': callback.from_user.id,
    }
    send_message_to_queue(message=ujson.dumps(message))
    await callback.message.edit_text(text='Мониторинг остановлен', reply_markup=back_kb())


def user_handlers(dp: Dispatcher):
    dp.message.register(start_menu, F.text == '/start')
    dp.callback_query.register(start_menu_cb, F.data == 'back')
    dp.callback_query.register(start_bot, F.data == 'start')
    dp.callback_query.register(stop_bot, F.data == 'stop')
