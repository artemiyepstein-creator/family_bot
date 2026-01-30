import asyncio # Импортируем из библиотеки инструмент для ассинхронного выполнения команд (чтобы когда бот думал он одновременно мог работать с командами)

from aiogram import Bot, Dispatcher # Импортируем из библиотеки инструменты для работы с ботом
from aiogram.fsm.storage.memory import MemoryStorage
from app.bot.routers.start import router
from app.bot.routers.shopping import router as shopping_router
from app.bot.routers.registration import router as registration_router


from app.config import get_settings
from app.db.session import create_engine, create_tables, create_sessionmaker



async def main():
    settings = get_settings()
    engine=create_engine(settings.database_url)  
    await create_tables(engine)

    sessionmaker = create_sessionmaker(engine)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.workflow_data["sessionmaker"] = sessionmaker
    dp.include_router(router)
    dp.include_router(shopping_router)
    dp.include_router(registration_router)
    
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

