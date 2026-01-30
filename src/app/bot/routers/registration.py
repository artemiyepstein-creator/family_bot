from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.services.member_service import MemberService
from app.bot.fsm.registration_states import RegistrationStates

router = Router()


@router.message(RegistrationStates.gender)
async def reg_gender(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()
    if text not in ("м", "ж"):
        await message.answer("Напиши 'м' или 'ж'")
        return

    await state.update_data(gender=text)
    await state.set_state(RegistrationStates.birth_date)
    await message.answer("Дата рождения (формат: ДД.ММ.ГГГГ)")


@router.message(RegistrationStates.birth_date)
async def reg_birth_date(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    try:
        birth_date = datetime.strptime(text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("Неверный формат. Пример: 12.03.2001")
        return

    await state.update_data(birth_date=birth_date)
    await state.set_state(RegistrationStates.short_name)
    await message.answer("Короткое имя (пример: Мама, Папа, Настя)")


@router.message(RegistrationStates.short_name)
async def reg_short_name(message: Message, state: FSMContext, **data):
    short_name = (message.text or "").strip()
    if not short_name:
        await message.answer("Короткое имя не может быть пустым")
        return

    sessionmaker = data["sessionmaker"]
    saved = await state.get_data()

    async with sessionmaker() as session:
        service = MemberService(session)
        await service.update_profile(
            family_id=message.chat.id,
            telegram_id=message.from_user.id,
            short_name=short_name,
            gender=saved["gender"],
            birth_date=saved["birth_date"],
        )

    await state.clear()
    await message.answer("Готово ✅ Регистрация завершена")