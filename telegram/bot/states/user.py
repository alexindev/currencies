from aiogram.fsm.state import StatesGroup, State


class Settings(StatesGroup):
    long_percent = State()
    long_time = State()
    short_percent = State()
    short_time = State()
