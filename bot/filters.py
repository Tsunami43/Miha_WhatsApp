from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):
    def __init__(self):
        self.admins = [422297622, "Kir_Miha"]

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins or message.from_user.username in self.admins

class Running(BaseFilter):
    def __init__(self)-> None: 
        self.state = False

    async def __call__(self, message: Message) -> bool:
        return self.state

RUNNING = Running()