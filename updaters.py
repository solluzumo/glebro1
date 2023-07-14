#Обновляет информацию о курсе депозита или курсе вывода в файле payment.txt. Принимает на вход имя курса и его новое значение.
async def update_rate_details(rate_name: str,rate_value:str):
    # Читаем содержимое файла rate.txt
    file = open("text/payment", 'r', encoding="utf8")
    content = file.read().split("\n")
    if rate_name.lower()=="депозит":
        updated_content = f"Курс депозита - {rate_value}р\n{content[1]}"
    if rate_name.lower()=="вывод":
        updated_content = f"{content[0]}\nКурс вывода - {rate_value}р"
    # Записываем обновленное содержимое обратно в файл rate.txt
    file = open("text/payment", 'w', encoding="utf8")
    file.write(updated_content)
    file.close()

#Обновляет реквизиты банка в файле rate.txt. Принимает на вход название банка, новый номер счета, новый телефон и новое контактное лицо.
async def update_bank_details(bank_name: str, account_number: str, phone: str, contact_person: str):
    # Читаем содержимое файла rate.txt
    file = open("text/rate", 'r', encoding="utf8")
    content = file.read()

    # Заменяем реквизиты банка в тексте
    bank_start_index = content.find(bank_name)
    if bank_start_index == -1:
        return
    bank_end_index = content.find('------------', bank_start_index)
    if bank_end_index == -1:
        return

    old_details = content[bank_start_index:bank_end_index]
    new_details = f'{bank_name}:\n{account_number}\n{phone}\n{contact_person}\n'

    updated_content = content.replace(old_details, new_details)

    # Записываем обновленное содержимое обратно в файл rate.txt
    file = open("text/rate", 'w', encoding="utf8")
    file.write(updated_content)
    file.close()

# Добавляет новые реквизиты банка в файл rate.txt. Принимает на вход название банка, номер счета, телефон и контактное лицо.
async def add_bank_details(bank_name: str, account_number: str, phone: str, contact_person: str):
    # Читаем содержимое файла rate.txt
    file = open("text/rate", encoding="utf8")
    content = file.read()

    # Добавляем новые реквизиты банка в текст
    new_details = f'{bank_name}:\n{account_number}\n{phone}\n{contact_person}\n------------\n'

    updated_content = content + new_details

    # Записываем обновленное содержимое обратно в файл rate.txt
    file = open("text/rate", 'w', encoding="utf8")
    file.write(updated_content)
    file.close()
