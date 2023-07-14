from aiogram.dispatcher.filters.state import State, StatesGroup

#Состояния
class AddBankState(StatesGroup):
    ENTER_DETAILS = State()

class EditBankState(StatesGroup):
    SELECT_BANK = State()
    ENTER_DETAILS = State()

class EditRateState(StatesGroup):
    SELECT_RATE = State()
    ENTER_DETAILS = State()