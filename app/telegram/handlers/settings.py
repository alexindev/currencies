from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from app.telegram.loader import db
from app.telegram.keyboars.inline import settings_kb, back_to_settings_kb
from app.telegram.services.helper import current_settings_text
from app.telegram.states.user import Settings


async def settings_menu(callback: types.CallbackQuery, state: FSMContext):
    """ Меню настроек """
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("Меню настроек", reply_markup=settings_kb())


async def long_percent(callback: types.CallbackQuery, state: FSMContext):
    """ Настройки % лонг """
    await callback.answer()
    await callback.message.edit_text("Укажите процент изменений. Например: 10", reply_markup=back_to_settings_kb())
    await state.set_state(Settings.long_percent)


async def long_percent_save(message: types.Message, state: FSMContext):
    """ Сохранить % лонг """
    try:
        percent = int(message.text)
        db.update_user(chat_id=message.from_user.id, long_percent=percent)
        await message.reply(f'Сохраняем. {percent}%', reply_markup=back_to_settings_kb())
        await state.clear()
    except ValueError:
        await message.reply('Введите число. Например: 10')


async def long_time(callback: types.CallbackQuery, state: FSMContext):
    """ Настройки времени long """
    await callback.answer()
    await callback.message.edit_text("Укажите время для отслеживания изменений в минутах. Например: 15",
                                     reply_markup=back_to_settings_kb())
    await state.set_state(Settings.long_time)


async def long_time_save(message: types.Message, state: FSMContext):
    """ Сохранить время лонг """
    try:
        time = int(message.text)
        await message.reply(f'Сохраняем. {time} мин', reply_markup=back_to_settings_kb())
        db.update_user(chat_id=message.from_user.id, long_time=time)
        await state.clear()
    except ValueError:
        await message.reply('Введите число. Например: 5')


async def short_percent(callback: types.CallbackQuery, state: FSMContext):
    """ Настройки % шорт """
    await callback.answer()
    await callback.message.edit_text("Укажите процент изменений. Например: 10", reply_markup=back_to_settings_kb())
    await state.set_state(Settings.short_percent)


async def short_percent_save(message: types.Message, state: FSMContext):
    """ Сохранить % шорт """
    try:
        percent = int(message.text)
        await message.reply(f'Сохраняем. {percent}%', reply_markup=back_to_settings_kb())
        db.update_user(chat_id=message.from_user.id, short_percent=percent)
        await state.clear()
    except ValueError:
        await message.reply('Введите число. Например: 10')


async def short_time(callback: types.CallbackQuery, state: FSMContext):
    """ Настройки времени шорт """
    await callback.answer()
    await callback.message.edit_text("Укажите время для отслеживания изменений в минутах. Например: 15",
                                     reply_markup=back_to_settings_kb())
    await state.set_state(Settings.short_time)


async def short_time_save(message: types.Message, state: FSMContext):
    """ Сохранить время шорт """
    try:
        time = int(message.text)
        await message.reply(f'Сохраняем. {time} мин', reply_markup=back_to_settings_kb())
        db.update_user(chat_id=message.from_user.id, short_time=time)
        await state.clear()
    except ValueError:
        await message.reply('Введите число. Например: 5')


async def current_setings(callback: types.CallbackQuery):
    """ Текущие заданные настройки """
    await callback.answer()

    data = db.get_user(chat_id=callback.from_user.id)
    if data:
        await callback.message.edit_text(text=current_settings_text(data), reply_markup=back_to_settings_kb())
    else:
        await callback.message.edit_text(text='Сначала зарегистрируйтесь: /start', reply_markup=back_to_settings_kb())


def settings_handlers(dp: Dispatcher):
    dp.callback_query.register(settings_menu, F.data == 'settings')
    dp.callback_query.register(current_setings, F.data == 'current_settings')
    dp.callback_query.register(long_percent, F.data == 'long_percent')
    dp.message.register(long_percent_save, Settings.long_percent)
    dp.message.register(long_time_save, Settings.long_time)
    dp.message.register(short_percent_save, Settings.short_percent)
    dp.message.register(short_time_save, Settings.short_time)
    dp.callback_query.register(long_time, F.data == 'long_time')
    dp.callback_query.register(short_percent, F.data == 'short_percent')
    dp.callback_query.register(short_time, F.data == 'short_time')
