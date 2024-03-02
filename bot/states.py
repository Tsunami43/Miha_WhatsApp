from aiogram.filters.state import State, StatesGroup


class Account(StatesGroup):
    menu = State()
    input_phone = State()

class TJson(StatesGroup):
    file = State()