from aiogram import types, Dispatcher, F

from loader import bot, db
from bot.keyboars.inline import main_kb, back_kb


async def start_menu(message: types.Message):
    """ Стартовое сообщение """
    db.new_user(chat_id=message.from_user.id)
    await bot.send_message(message.from_user.id, text="Главное меню:", reply_markup=main_kb())


async def market_menu(callback: types.CallbackQuery):
    """ Меню биржи """
    await callback.answer()
    await callback.message.edit_text("Биржи будут тут", reply_markup=back_kb())


async def start_menu_cb(callback: types.CallbackQuery):
    """ Стартовое сообщение c callback"""
    await callback.answer()
    await callback.message.edit_text(text="Выберите меню:", reply_markup=main_kb())


def user_handlers(dp: Dispatcher):
    dp.message.register(start_menu, F.text == '/start')
    dp.callback_query.register(market_menu, F.data == 'market')
    dp.callback_query.register(start_menu_cb, F.data == 'back')
