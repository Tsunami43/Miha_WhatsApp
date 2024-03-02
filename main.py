from pathlib import Path
# директория под логи
Path("logs").mkdir(parents=True, exist_ok=True)

import asyncio, logging, bot
from utils import config
from green_api import instance

async def main():
    logging.basicConfig(level=logging.INFO)
    await  bot.run(config.get('Telegram','token'))

    

    
if __name__ == "__main__":
    asyncio.run(main())