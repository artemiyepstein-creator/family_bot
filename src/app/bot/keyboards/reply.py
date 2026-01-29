from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Добавить покупку")],
            [KeyboardButton(text="🧾 Список покупок")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери действие",
        is_persistent=True,
    )
