from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.filters import AdminFilter, RUNNING
from bot.states import Account, TJson

from os import remove
import json

from green_api import instance
from green_api.types.objects import Message as WA_Message


from utils.loggers import target_logger
logger = target_logger(__name__)

router = Router()


@router.message(AdminFilter(), StateFilter(None), F.text=="👤 Настройки аккаунта 👤")
async def setting_handler(message: Message, state: FSMContext):
    await state.set_state(Account.menu)
    await message.answer(
        text=
            "<b>Используйте кнопку статуса для просмотра состояния аккаунта.</b>\n\n"+
            "<b>-</b>Если аккаунт не авторизован, вам следует его добавить.\n"+
            "<b>-</b>Для смены аккаунта, требуется разлогинить его и проверить статус авторизации."
        ,
        reply_markup=keyboards.account()
    )

@router.message(AdminFilter(), StateFilter(None), F.text=="💬 Добавить вопрос ответ 💬")
async def new_text_handler(message: Message, state: FSMContext):
    await state.set_state(TJson.file)
    await message.answer(
        text=
            "Для того чтобы изменить формат вопросов ответов, скиньте <b>json</b> файл:"
        ,
        reply_markup=keyboards.cancel()
    )

@router.message(AdminFilter(), TJson.file, F.text=="🚫 Отмена 🚫")
async def cancel_json_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Действие отменено!</b>",
        reply_markup=keyboards.menu()
    )

@router.message(AdminFilter(), TJson.file, F.document.mime_type=="application/json")
async def json_handler(message: Message, state: FSMContext, bot: Bot):
    try:
        path = "bot/assets/q&a.json"
        remove(path)
        file = await bot.get_file(message.document.file_id)
        await bot.download_file(file.file_path, path)
        await message.answer(
            "<b>Успех!</b> Изменения вступят в силу при следующем запуске.",
            reply_markup=keyboards.menu()
        )
    except:
        await message.answer(
            "<b>Ошибка!</b>",
            reply_markup=keyboards.menu()
        )
    finally:
        await state.clear()


@router.message(AdminFilter(), StateFilter(None), F.text=="🟢 Запустить", RUNNING)
async def run_handler(message: Message):
    await message.answer(
        "🟢 Уже запущен 🟢"
    )


@router.message(AdminFilter(), StateFilter(None), F.text=="🟢 Запустить")
async def run_handler(message: Message): 

    RUNNING.state = True
    try:
        if await instance.get_state_instance():
            await message.answer(
                "🟢 <b>WhatsApp запущен</b>"
            )

            with open("bot/assets/q&a.json") as json_data:
                data = json.load(json_data)

            while RUNNING.state:
                wa_message = await instance.receive_notification()
                
                if isinstance(wa_message, WA_Message):
                    
                    text = "The question is clear. Unfortunately, I have to leave immediately. I'll get back to you later."

                    for key in data:
                        if key in wa_message.text.lower():
                            text = data[key]
                            break
                        
                    try:
                        await instance.send_message(
                            chat_id=wa_message.chat_id,
                            text=text,
                            reply_message_id=wa_message.message_id
                        )
                    except Exception as ex:
                        logger.error(ex)

            await message.answer(
                "🔴 <b>WhatsApp отключен</b>"
            )

        else:
            RUNNING.state = False
            await message.answer(
                "<b>Неполадки с аккаунтом!</b> Проверьте статус авторизации."
            )

    except Exception as ex:
        logger.error(ex)
        RUNNING.state = False
        await message.answer(
            "<b>Неполадки с аккаунтом!</b> Проверьте статус авторизации."
        )

@router.message(AdminFilter(), StateFilter(None), F.text=="🔴 Остановить", RUNNING)
async def stop1_handler(message: Message):
    RUNNING.state = False
    await message.answer(
        "Останавливаем"
    )


@router.message(AdminFilter(), StateFilter(None), F.text=="🔴 Остановить")
async def stop2_handler(message: Message):
    await message.answer(
        "🔴 Не запущен 🔴"
    )