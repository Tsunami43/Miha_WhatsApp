from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import routers
from bot.ui_commands import set_bot_commands

async def run(token: str):

    bot = Bot(token, parse_mode="HTML")

    dp = Dispatcher(storage=MemoryStorage())
    await bot.delete_webhook(drop_pending_updates=True) 

    dp.message.filter(F.chat.type == "private")

    dp.include_routers(*routers)
    
    await set_bot_commands(bot)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()