from pathlib import Path
# директория под логи
Path("logs").mkdir(parents=True, exist_ok=True)

import asyncio, logging, bot
from utils import config
from utils.loggers import main_logger


async def main():
    main_logger()
    await  bot.run(config.get('Telegram','token'))

    
if __name__ == "__main__":
    asyncio.run(main())