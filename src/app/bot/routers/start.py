from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from typing import Any
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram.fsm.context import FSMContext


from app.services.family_service import FamilyService
from app.services.member_service import MemberService
from app.bot.fsm.registration_states import RegistrationStates
from app.db.session import create_sessionmaker
from app.bot.keyboards.reply import main_menu_kb

router = Router()

@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext, **data: Any):
    chat = message.chat

    if chat.type not in ("group", "supergroup"):
        await message.answer("Добавь меня в семейный чат 🙂")
        return

    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    async with sessionmaker() as session:
        service = FamilyService(session)
        await service.ensure_family_exists(
            family_id=chat.id,
            title=chat.title or "Без названия",
        )

        user = message.from_user
        member_sevice = MemberService(session)

        role = await member_sevice.ensure_member_exists(
            family_id=chat.id,
            telegram_id=user.id,
            full_name=user.full_name,
            username=user.username,
        )
        if role == "owner":
            await message.answer("Семья зарегистрирована. Ты владелец 👑")
        else:
            await message.answer("Ты добавлен(а) в семью 👋")

        member = await member_sevice.get_member(chat.id, user.id)

        # если профиль не заполнен — запускаем регистрацию
        if member.short_name is None:
            await message.answer("Давай коротко зарегистрируемся. Пол? (м / ж)")
            await state.set_state(RegistrationStates.gender)
            return
        
        await message.answer("Меню:", reply_markup=main_menu_kb())

        

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Меню:", reply_markup=main_menu_kb())
