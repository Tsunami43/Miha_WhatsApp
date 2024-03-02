from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

def menu()-> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🟢 Запустить"),
        KeyboardButton(text="🔴 Остановить")
    )
    builder.row(
        KeyboardButton(text="👤 Настройки аккаунта 👤")
    )
    builder.row(
        KeyboardButton(text="💬 Добавить вопрос ответ 💬")
    )
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Если не видно кнопок 👉🏻"
    )


def account():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Вернуться в главное меню")
    )
    builder.row(
        KeyboardButton(text="🌐 Статус"),
        KeyboardButton(text="🗑 Разлогинить")
    )
    builder.row(
        KeyboardButton(text="♻️ Добавить|сменить аккаунт ♻️")
    )
    # builder.row(
        
    # )
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Если не видно кнопок 👉🏻"
    )


def cancel()-> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🚫 Отмена 🚫")
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Если не видно кнопок 👉🏻"
    )

def yes_or_no():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Да",
            callback_data="yes"
        ),
        InlineKeyboardButton(
            text="Нет",
            callback_data="no"
        )
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)