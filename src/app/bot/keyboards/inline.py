from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.callbacks import ShopCB


def shopping_item_kb(item_id: int, is_done: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if not is_done:
        kb.button(text="✅ Куплено", callback_data=ShopCB(action="done", item_id=item_id).pack())
    else:
        kb.button(text="↩ Вернуть", callback_data=ShopCB(action="undone", item_id=item_id).pack())

    kb.button(text="🗑 Удалить", callback_data=ShopCB(action="del", item_id=item_id).pack())

    kb.adjust(2)
    return kb.as_markup()