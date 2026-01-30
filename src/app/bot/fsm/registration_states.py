from aiogram.fsm.state import StatesGroup, State

class RegistrationStates (StatesGroup):
    gender = State()
    birth_date = State()
    short_name = State()