from typing import Any

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.services.shopping_service import ShoppingService
from app.bot.keyboards.inline import shopping_item_kb
from app.bot.fsm.shopping_states import ShoppingStates
from app.bot.callbacks import ShopCB
from app.bot.keyboards.reply import main_menu_kb
from app.services.family_service import FamilyService

router = Router()

@router.message(ShoppingStates.waiting_title)
async def add_from_text(message: Message, state: FSMContext, **data: Any):
    if not _ensure_group(message):
        await state.clear()
        await message.answer("Команда работает только в группе.")
        return

    raw = (message.text or "").strip()
    if not raw:
        await message.answer("Пусто. Напиши название покупки (или несколько через запятую).")
        return

    # 1) режем по запятым
    parts = [p.strip() for p in raw.split(",")]
    # 2) убираем пустые
    titles = [p for p in parts if p]
    titles = [t[:1].upper() + t[1:] if t else t for t in titles]

    if not titles:
        await message.answer("Не вижу названий. Пример: молоко, хлеб, яйца")
        return
    if "sessionmaker" not in data:
        await message.answer("DEBUG: sessionmaker НЕ ПРИШЁЛ в data")
        return

    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    added_ids: list[int] = []
    async with sessionmaker() as session:
        family_service = FamilyService(session)
        await family_service.ensure_family_exists(
        family_id=message.chat.id,
        title=message.chat.title or "Без названия",
    )
        
        service = ShoppingService(session)

        # добавляем каждую позицию
        for title in titles:
            item = await service.add(
                family_id=message.chat.id,
                user_id=message.from_user.id,
                title=title,
            )
            added_ids.append(item.id)

    await state.clear()

    if len(titles) == 1:
        await message.answer(f"Добавил: {titles[0]}")
    else:
        await message.answer(
            "Добавил:\n" + "\n".join(f"• {t}" for t in titles)
        )
    
    await message.answer("Готово ✅", reply_markup=main_menu_kb())


def _ensure_group(message: Message) -> bool:
    return message.chat.type in ("group", "supergroup")


@router.message(Command("buy"))
async def cmd_buy(message: Message, **data: Any):
    if not _ensure_group(message):
        await message.answer("Команда работает только в группе.")
        return

    text = (message.text or "").strip()
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Напиши так: /buy молоко")
        return

    title = parts[1]
    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    async with sessionmaker() as session:
        service = ShoppingService(session)
        item = await service.add(family_id=message.chat.id, user_id=message.from_user.id, title=title)

    await message.answer(f"Добавил: {item.title}")


@router.message(Command("list"))
async def cmd_list(message: Message, **data: Any):
    if not _ensure_group(message):
        await message.answer("Команда работает только в группе.")
        return

    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]
    async with sessionmaker() as session:
        service = ShoppingService(session)
        items = await service.list_open(family_id=message.chat.id)

    if not items:
        await message.answer("Список покупок пуст.")
        return

    await message.answer("Список покупок:")
    for it in items:
        await message.answer(
            f"{it.title}",
            reply_markup=shopping_item_kb(item_id=it.id, is_done=it.is_done),
        )


@router.message(Command("done"))
async def cmd_done(message: Message, **data: Any):
    if not _ensure_group(message):
        await message.answer("Команда работает только в группе.")
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Напиши так: /done 3")
        return

    item_id = int(parts[1])
    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    async with sessionmaker() as session:
        service = ShoppingService(session)
        ok = await service.done(family_id=message.chat.id, item_id=item_id)

    await message.answer("Отметил как куплено." if ok else "Не нашёл такой id в этой семье.")


@router.message(Command("undone"))
async def cmd_undone(message: Message, **data: Any):
    if not _ensure_group(message):
        await message.answer("Команда работает только в группе.")
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Напиши так: /undone 3")
        return

    item_id = int(parts[1])
    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    async with sessionmaker() as session:
        service = ShoppingService(session)
        ok = await service.undone(family_id=message.chat.id, item_id=item_id)

    await message.answer("Вернул в список." if ok else "Не нашёл такой id в этой семье.")


@router.message(Command("del"))
async def cmd_del(message: Message, **data: Any):
    if not _ensure_group(message):
        await message.answer("Команда работает только в группе.")
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Напиши так: /del 3")
        return

    item_id = int(parts[1])
    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    async with sessionmaker() as session:
        service = ShoppingService(session)
        ok = await service.delete(family_id=message.chat.id, item_id=item_id)

    await message.answer("Удалил." if ok else "Не нашёл такой id в этой семье.")


@router.message(F.text == "🧾 Список покупок")
async def txt_list(message: Message, **data: Any):
    await cmd_list(message, **data)

@router.message(F.text == "➕ Добавить покупку")
async def txt_add(message: Message, state: FSMContext):
    if not _ensure_group(message):
        await message.answer("Команда работает только в группе.")
        return
    await state.set_state(ShoppingStates.waiting_title)
    await message.answer(
        "Напиши покупки через запятую.\nПример: молоко, хлеб, яйца",
        reply_markup=ReplyKeyboardRemove()
        )


@router.callback_query(ShopCB.filter())
async def shop_callback(query: CallbackQuery, callback_data: ShopCB, **data: Any):
    if not query.message:
        await query.answer()
        return

    family_id = query.message.chat.id
    sessionmaker: async_sessionmaker[AsyncSession] = data["sessionmaker"]

    async with sessionmaker() as session:
        service = ShoppingService(session)

        if callback_data.action == "done":
            ok = await service.done(family_id=family_id, item_id=callback_data.item_id)
            text = "Отметил как куплено." if ok else "Не нашёл."
        elif callback_data.action == "undone":
            ok = await service.undone(family_id=family_id, item_id=callback_data.item_id)
            text = "Вернул в список." if ok else "Не нашёл."
        elif callback_data.action == "del":
            ok = await service.delete(family_id=family_id, item_id=callback_data.item_id)
            text = "Удалил." if ok else "Не нашёл."
        else:
            ok = False
            text = "Неизвестное действие."

    # UX: если удалили — убираем сообщение
    if callback_data.action == "del" and ok:
        await query.message.delete()
    else:
        await query.answer(text)
