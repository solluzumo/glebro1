from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import re
from aiogram.dispatcher import FSMContext
from states import *
from keyboards import *
from updaters import *
import os
API_TOKEN = os.getenv("TOKEN")
admin_id = open("text/admins", "r").read().split("\n")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


#Присылает пользователю "акутальный курс"
@dp.message_handler(commands=['payment'])
async def send_payment(message: types.Message):
    payment_text = open("text/payment", encoding="utf-8").read()
    await message.answer("Актуальный курс за 1$:\n"+payment_text)


#Присылает пользователю "актуальные реквизиты"
@dp.message_handler(commands=['rates'])
async def send_rates(message: types.Message):
    rate_text = open("text/rate", encoding="utf-8").read()
    await message.answer("Реквизиты для оплаты:\n"+rate_text.replace("------------","\n"))


#Присылает пользователю приветствие
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_text = open("text/welcome", encoding="utf-8").read()
    additional_text=""
    if str(message.from_user.id) in admin_id:
        additional_text="\nВы являетесь администратором, вот список доступных вам комманд:\n" \
                        "/edit_rate - изменить курс депозита и вывода средств\n"\
                         "/edit_bank - изменить реквезиты конкретного банка\n" \
                        "/add_bank - добавить новые реквизиты\n" \
                        "/delete_bank - удалить реквизиты конкретного банка\n"
    await message.answer(welcome_text+additional_text)


#Начало сценария изменения данных одного из курсов
@dp.message_handler(commands=['edit_rate'])
async def edit_rate_handler(message: types.Message):
    if str(message.from_user.id) not in admin_id:
        await message.reply(f'У вас нет доступа к этой команде.')
        return

    keyboard = get_rate_keyboard()
    await message.reply('Выберите поле для изменения:', reply_markup=keyboard)


#Начало сценария изменения данных одного из реквизитов
@dp.message_handler(commands=['edit_bank'])
async def edit_bank_handler(message: types.Message):
    if str(message.from_user.id) not in admin_id:
        await message.reply(f'У вас нет доступа к этой команде.')
        return
    banks = get_available_banks()  # Получаем доступные банки из файла rate.txt

    if not banks:
        await message.reply('Нет доступных банков для редактирования.')
        return

    keyboard = get_bank_keyboard(banks)
    await message.reply('Выберите банк, реквизиты которого вы хотите изменить:', reply_markup=keyboard)


#Начало сценария удаления данных одного из реквизитов
@dp.message_handler(commands=['delete_bank'])
async def delete_bank_handler(message: types.Message):
    if str(message.from_user.id) not in admin_id:
        await message.reply(f'У вас нет доступа к этой команде.')
        return
    banks = get_available_banks()  # Получаем доступные банки из файла rate.txt

    if not banks:
        await message.reply('Нет доступных банков для редактирования.')
        return

    keyboard = get_deliting_keyboard(banks)

    await message.reply('Выберите банк, реквизиты которого вы хотите удалить:', reply_markup=keyboard)


#Начало сценария удаления данных одного из администраторов(сценарий не доделан)
@dp.message_handler(commands=['delete_admin_id'])
async def delete_admin_handler(message: types.Message):
    admins = admin_id

    keyboard = get_deliting_admin_keyboard(admins)

    await message.reply('Выберите админа,которого вы хотите удалить:', reply_markup=keyboard)


#Начало сценария добавления новых реквизитов
@dp.message_handler(commands=['add_bank'])
async def add_bank_handler(message: types.Message):
    if str(message.from_user.id) not in admin_id:
        await message.reply('У вас нет доступа к этой команде.')
        return

    await message.reply('Введите новые реквизиты банка в формате:\n\n'
                        'Название банка:\nНомер счета:\nТелефон:\nКонтактное лицо:')

    # Устанавливаем состояние для обработки следующего сообщения
    await AddBankState.ENTER_DETAILS.set()


#Получение и проверка данных для новых реквизитов
@dp.message_handler(state=AddBankState.ENTER_DETAILS)
async def add_bank_details_handler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in admin_id:
        await message.reply('У вас нет доступа к этой команде.')
        return

    lines = message.text.split('\n')

    if len(lines) < 4:
        await message.reply('Пожалуйста, отправьте новые реквизиты в правильном формате.')
        return

    bank_name = lines[0].strip()
    account_number = lines[1].strip()
    phone = lines[2].strip()
    contact_person = lines[3].strip()

    await add_bank_details(bank_name, account_number, phone, contact_person)

    await message.reply('Реквизиты банка успешно добавлены.')

    # Сбрасываем состояние FSM
    await state.finish()


#Получение данных о выбранных для изменения реквизитах
@dp.callback_query_handler(lambda c: c.data.startswith('edit_bank:'))
async def edit_bank_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    bank_name = callback_query.data.split(':')[1]
    await callback_query.message.reply(f'Вы выбрали банк: {bank_name.rstrip()}. '
                                       f'Отправьте новые реквизиты в формате:\n\n'
                                       f'\nНомер счета:\nТелефон:\nКонтактное лицо:')

    await callback_query.answer()

    # Устанавливаем состояние для обработки следующего сообщения
    await EditBankState.ENTER_DETAILS.set()

    # Сохраняем выбранный банк в состоянии FSM
    await state.update_data(bank_name=bank_name)


#Получение данных о выбранном для изменения курсе
@dp.callback_query_handler(lambda c: c.data.startswith('edit_rate:'))
async def edit_rate_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    rate_name = callback_query.data.split(':')[1]
    await callback_query.message.reply(f'Отправьте новое значение для {rate_name} за 1$')

    await callback_query.answer()

    # Устанавливаем состояние для обработки следующего сообщения
    await EditRateState.ENTER_DETAILS.set()

    # Сохраняем выбранный банк в состоянии FSM
    await state.update_data(rate_name=rate_name)


#Получение данных о выбранных для изменения реквизитах
@dp.message_handler(state=EditRateState.ENTER_DETAILS)
async def update_rate_handler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in admin_id:
        await message.reply('У вас нет доступа к этой команде.')
        return

    data = await state.get_data()
    rate_name = data.get('rate_name')
    lines = message.text.split('\n')
    rate_value = lines[0]

    await update_rate_details(rate_name,rate_value)

    await message.reply(f'Курс {rate_name.lower()} успешно изменён.')

    # Сбрасываем состояние FSM
    await state.finish()


#Получение и проверка данных для изменения реквизитов
@dp.message_handler(state=EditBankState.ENTER_DETAILS)
async def update_bank_handler(message: types.Message, state: FSMContext):
    if str(message.from_user.id) not in admin_id:
        await message.reply('У вас нет доступа к этой команде.')
        return

    lines = message.text.split('\n')

    if len(lines) < 3:
        await message.reply('Пожалуйста, отправьте новые реквизиты в правильном формате.')
        return

    data = await state.get_data()
    bank_name = data.get('bank_name')
    account_number = lines[0].strip()
    phone = lines[1].strip()
    contact_person = lines[2].strip()
    await update_bank_details(bank_name, account_number, phone, contact_person)

    await message.reply('Реквизиты банка успешно обновлены.')

    # Сбрасываем состояние FSM
    await state.finish()


#Удаление выбранного банка и изменение файла с информацией о данном банке
@dp.callback_query_handler(lambda c: c.data.startswith('delete_bank:'))
async def delete_bank_details(callback_query: types.CallbackQuery):
    # Читаем содержимое файла rate.txt
    bank_name = callback_query.data.split(':')[1]
    file = open("text/rate", encoding="utf8")
    content = file.read()

    # Удаляем реквизиты банка из текста
    bank_start_index = content.find(bank_name)
    if bank_start_index == -1:
        return

    bank_end_index = content.find('------------', bank_start_index)
    if bank_end_index == -1:
        return

    old_details = content[bank_start_index:bank_end_index+13]
    updated_content = content.replace(old_details, '')
    # Записываем обновленное содержимое обратно в файл rate.txt
    file = open("text/rate", 'w', encoding="utf8")
    file.write(updated_content)
    file.close()
    await callback_query.message.reply(f'Банк {bank_name} был успешно удалён!')


#Удаление выбранного администратора(не сделано)
@dp.callback_query_handler(lambda c: c.data.startswith('delete_admin:'))
async def delete_admin_details(callback_query: types.CallbackQuery):

    deliting_admin_id = callback_query.data.split(':')[1]
    file = open("text/admins", encoding="utf8")
    content = file.read()

    updated_content = content.replace(deliting_admin_id, '')

    # Записываем обновленное содержимое обратно в файл rate.txt
    file = open("text/rate", 'w', encoding="utf8")
    file.write(updated_content)
    file.close()
    await callback_query.message.reply(f'Админ с {deliting_admin_id} был успешно удалён!')


#Получение доступных для изменения/удаления реквизитов
def get_available_banks():
    file = open("text/rate", encoding="utf8")
    content = file.read()

    banks = re.findall(r'^([А-Яа-я\s]+):', content, flags=re.MULTILINE)
    return banks


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
