from asyncio import sleep
from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from bot import keyboards
from bot.filters import AdminFilter
from bot.states import Account

from green_api import instance

router = Router()


@router.message(AdminFilter(), Account.menu, F.text=="Вернуться в главное меню")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=
            "<u>Справка:</u>\n\n"+
            "Для запуска и остановки автоответа в WhatsApp используйте соотвествующие кнопки.\n<i>(Если аккаунт не добавлен, то запуск не произведется)</i>\n\n"+
            "<b>Настройка аккаунта</b> - Для добавления|удаления|смены аккаунта, а также просмотра статуса авторизации"+
            "Для добавления вопрос ответов, используйте соотвествующую кнопку и следуйте инструкциям."
        ,
        reply_markup=keyboards.menu()
    )


@router.message(AdminFilter(), Account.menu, F.text=="🌐 Статус")
async def status_handler(message: Message):
    status = await instance.get_wa_status()
    if status.is_closed:
        await message.answer(
            "<b>Ошибка!</b>\n"+status.message
        )
    else:
        await message.answer(
            status.message
        )


@router.message(AdminFilter(), Account.menu, F.text=="🗑 Разлогинить")
async def logout_handler(message: Message):
    await message.answer(
        "Вы уверены что хотите разлогинить аккаунт?",
        reply_markup=keyboards.yes_or_no()
    )

@router.callback_query(F.data=="yes")
async def yes_logout(call: CallbackQuery):
    logout = await instance.wa_log_out()
    if logout:
        await call.message.edit_text(
            "<b>Успешно!</b>"
        )
    else:
        await call.message.edit_text(
            "<b>Ошибка!</b>"
        )


@router.callback_query(F.data=="no")
async def no_logout(call: CallbackQuery):
    await call.message.edit_text(
        "<b>Действие отменено!</b>"
    )



@router.message(AdminFilter(), Account.menu, F.text=="♻️ Добавить|сменить аккаунт ♻️")
async def new_acc_handler(message: Message, state: FSMContext):
    await state.set_state(Account.input_phone)
    await message.answer(
            "<b>Введите номер телефона</b> в международном формате без + и 00\n<i>пример: 31684085474</i>",
            reply_markup=keyboards.cancel()
        )


@router.message(AdminFilter(), Account.input_phone, F.text=="🚫 Отмена 🚫")
async def cancel_handler(message: Message, state: FSMContext):
    await state.set_state(Account.menu)
    await message.answer(
        text=
            "<b>Используйте кнопку статуса для просмотра состояния аккаунта.</b>\n\n"+
            "<b>-</b>Если аккаунт не авторизован, вам следует его добавить.\n"+
            "<b>-</b>Для смены аккаунта, требуется разлогинить его и проверить статус авторизации."
        ,
        reply_markup=keyboards.account()
    )


@router.message(AdminFilter(), Account.input_phone, F.text)
async def phone_handler(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        msg = await message.answer(
            "<b>Ожидайте!</b> Генерируем код для авторизации...",
            reply_markup=ReplyKeyboardRemove()
        )
        try:
            code = await instance.authorization_code(int(message.text))
            if code:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=msg.message_id    
                )
                await message.answer_photo(
                    FSInputFile("bot/assets/1.png"),
                    caption=
                        f"Для авторизации аккаунта\n👤 +{message.text}\n\nКод: <b>{code}</b>",
                    reply_markup=keyboards.account()
                    
                )
                await state.set_state(Account.menu)

            else:
                await state.set_state(Account.menu)
                await message.answer(
                    "<b>Ошибка!</b>",
                    reply_markup=keyboards.account()
                )
        except:
            await state.set_state(Account.menu)
            await message.answer(
                "<b>Ошибка!</b> Возможно вы не разлогинились.",
                reply_markup=keyboards.account()
            )
    else:
        await message.answer(
            "<b>Ошибка ввода!</b>\nПовторите попытку..."
        ) 
