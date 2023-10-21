# Чат-бот

### Описание проекта

Данный чат-бот присылает реквизиты для перевода средств, актуальный курс. Для чат-бота реализована админ-панель, позволяющая редактировать реквизиты, курс.

### Устройство проекта

Проект имеет следующую структуру:
1. `server.py`: Файл с хэндлерами для обработки запросов пользователя (текстовые запросы и обработка клавиатуры) и запросов администратора.
2. `keyboards.py`: Файл, формирующий клавиатуру для удобного взаимодействия с пользователем.
3. `states.py`: Файл, описывающий состояния.
4. `updaters.py`: Файл, обновляющий файлы payment и rate.
   
### Запуск проекта

Для запуска проекта необходимо установить все зависимости из файла `requirements.txt` и запустить бота командой `python main.py`.

### Зависимости

Проект использует следующие зависимости:
- `aiogram`: библиотека для создания ботов Telegram.

### Функционал проекта

1. Отправка курса и реквизитов, используя комманды /rate и /payment.

2. Админ панель: бот имеет админ панель, которая содержит функции изменения файлов `text/rate` и `text/payment`, пользоваться ей могут только те пользователи, чей id хранится в файле `text/admins`, функции дающие и лищающие права администратора не были реализованы.

### Устройство файлов

Проект содержит несколько файлов с данными:
1. Файл `text/rate` содержит курс обмена.
2. Файл `text/rate` содержит реквизиты для оплаты. 
