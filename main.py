import logging
logging.basicConfig(filename='runtime.log', encoding='utf-8', level=logging.INFO)

from asyncio import run, TaskGroup
from configs import configs
from datetime import datetime
from tb_discord import bot
import server_data


# =======INIT=======

utc_start = datetime.utcnow()
print(f"Started at {str(utc_start)[:-16]}")
logging.info("Started on %s", utc_start.strftime('%d-%m-%Y at %H:%M:%S UTC%z'))

async def main():
    async def runner():
        async with bot:
            await bot.start(configs.TOKEN)

    async with TaskGroup() as tg:
        tg.create_task(server_data.loop())
        tg.create_task(runner())


run(main())
