from aiogram import types

def get_bank_keyboard(banks):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for bank in banks:
        button = types.InlineKeyboardButton(text=bank, callback_data=f'edit_bank:{bank}')
        keyboard.add(button)

    return keyboard

def get_rate_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    button1 = types.InlineKeyboardButton(text="Курс депозита", callback_data=f'edit_rate:Депозит')
    button2 = types.InlineKeyboardButton(text="Курс вывода", callback_data=f'edit_rate:Вывод')

    keyboard.add(button1)
    keyboard.add(button2)


    return keyboard

def get_deliting_keyboard(banks):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for bank in banks:
        button = types.InlineKeyboardButton(text=bank, callback_data=f'delete_bank:{bank}')
        keyboard.add(button)

    return keyboard

def get_deliting_admin_keyboard(admins):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for admin in admins:
        button = types.InlineKeyboardButton(text=admin, callback_data=f'delete_admin:{admin}')
        keyboard.add(button)

    return keyboard