from aiogram.filters.callback_data import CallbackData


class ShopCB(CallbackData, prefix="shop"):
    action: str   # done | undone | del
    item_id: int