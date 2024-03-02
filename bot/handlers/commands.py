from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.state import StateFilter

from bot import keyboards
from bot.filters import AdminFilter


router = Router()


@router.message(AdminFilter(), StateFilter(None), Command('start'))
async def start_handler(message: Message):
    await message.answer(
        text=
            "<u>Справка:</u>\n\n"+
            "Для запуска и остановки автоответа в WhatsApp используйте соотвествующие кнопки.\n<i>(Если аккаунт не добавлен, то запуск не произведется)</i>\n\n"+
            "<b>Настройка аккаунта</b> - Для добавления|удаления|смены аккаунта, а также просмотра статуса авторизации"+
            "Для добавления вопрос ответов, используйте соотвествующую кнопку и следуйте инструкциям."
        ,
        reply_markup=keyboards.menu()
    )