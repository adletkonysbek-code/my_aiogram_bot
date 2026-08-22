import asyncio
from aiogram import Bot, Dispatcher

from config import bot, dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.routes import send_story_to_channel
from handlers.routes import router

dp.include_router(router)
            
async def main():

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_story_to_channel, 'interval', seconds=45, args=[bot])
    scheduler.start()

    print("БОТ ЗАПУЩЕН!")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())