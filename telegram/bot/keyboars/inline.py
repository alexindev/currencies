from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    """ Главное меню """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='🏦 Биржи', callback_data='market')
    keyboard.button(text='🛠️ Настройки', callback_data='settings')
    keyboard.adjust(2)
    return keyboard.as_markup()


def settings_kb() -> InlineKeyboardMarkup:
    """ Клавиатура для настроек """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='🟢 Период лонг', callback_data='long_time')
    keyboard.button(text='➗ Процент лонг', callback_data='long_percent')
    keyboard.button(text='🔴 Период шорт', callback_data='short_time')
    keyboard.button(text='➗ Процент шорт', callback_data='short_percent')
    keyboard.button(text='♻️ Текущие настройки', callback_data='current_settings')
    keyboard.button(text='↩', callback_data='back')
    keyboard.adjust(2, 2, 1, 1)
    return keyboard.as_markup()


def back_kb() -> InlineKeyboardMarkup:
    """ Кнопка назад на главную """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='↩', callback_data='back')
    return keyboard.as_markup()


def back_to_settings_kb() -> InlineKeyboardMarkup:
    """ Кнопка назад в настройки """
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='↩', callback_data='settings')
    return keyboard.as_markup()
