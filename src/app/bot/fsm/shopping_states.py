from aiogram.fsm.state import StatesGroup, State


class ShoppingStates(StatesGroup):
    waiting_title = State()