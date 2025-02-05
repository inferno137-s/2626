import telebot
from telebot import types
from datetime import datetime, timedelta

bot = telebot.TeleBot('7677815065:AAHAJOUVybTC2VnUiK41dr9X7A3fl7NKmXE')

# States
STATE_PROFESSION = 0
STATE_PAYDAY = 1
STATE_SALARY = 2
STATE_FINISHED = 3

user_data = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "🎉 Привет! Добро пожаловать в наш бот где ты сможешь считать свой бюджет!")
    show_main_menu(message)


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Опрос"), types.KeyboardButton("Меню"), types.KeyboardButton("Профиль"))
    bot.send_message(message.chat.id, "Вы в главном меню. Выберите опцию:", reply_markup=markup)


def show_powerlifting_options(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "Мои деньги",
        "История расходов",
        "Календарь",
        "Ежедневной нормы расходов",
        "Советы",
        "🔙 Назад"
    ]
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    bot.send_message(message.chat.id, "Выберите одну из тем:", reply_markup=markup)


def send_excel_file(message):
    files = {
        "Мои деньги": "\\path_to_file\\Мои_деньги.xlsx",
        "История расходов": "\\path_to_file\\История_расходов.xlsx",
        "Календарь": "\\path_to_file\\Календарь.xlsx",
        "Ежедневной нормы расходов": "\\path_to_file\\Ежедневной_нормы_расходов.xlsx",
        "Советы": "\\path_to_file\\Советы.docx"
    }

    file_name = files.get(message.text)
    if file_name:
        try:
            with open(file_name, 'rb') as file:
                bot.send_document(message.chat.id, file)
                back_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back_markup.add(types.KeyboardButton("🔙 Назад"))
                bot.send_message(message.chat.id, "Вот файл. Нажмите 'Назад', чтобы вернуться.", reply_markup=back_markup)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Файл не найден. Проверьте путь.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Не удалось отправить файл: {str(e)}")


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        if message.text == "Меню":
            show_powerlifting_options(message)
        elif message.text == "История расходов":
            show_expense_history(message)
        elif message.text == "Календарь":
            show_salary_countdown(message)
        elif message.text == "Мои деньги":
            send_excel_file(message)
        elif message.text == "Ежедневной нормы расходов":
            send_excel_file(message)
        elif message.text == "Советы":
            send_excel_file(message)
        elif message.text == "🔙 Назад":
            show_main_menu(message)
        elif message.text == "Опрос":
            user_data[chat_id] = {}
            ask_profession(message)
        elif message.text == "Профиль":
            show_profile(message)


def show_salary_countdown(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id, {})
    
    if 'payday' in user_info:
        payday = int(user_info['payday'])
        today = datetime.today()
        next_salary_date = datetime(today.year, today.month, payday)

        if next_salary_date < today:
            
            if today.month == 12:
                next_salary_date = datetime(today.year + 1, 1, payday)
            else:
                next_salary_date = datetime(today.year, today.month + 1, payday)

        days_until_salary = (next_salary_date - today).days
        bot.send_message(chat_id, f"До следующей зарплаты осталось {days_until_salary} дней.")
    else:
        bot.send_message(chat_id, "Дата выплаты зарплаты не указана. Пройдите опрос, чтобы указать её.")


def show_expense_history(message):
    chat_id = message.chat.id
    expense_data = user_data.get(chat_id, {}).get('expenses', [])

    if expense_data:
        history_text = "🧾 История расходов:\n"
        for expense in expense_data:
            history_text += f"Дата: {expense['date']} - Сумма: {expense['amount']}₽\n"
    else:
        history_text = "История расходов пуста. Добавьте расходы, чтобы увидеть их здесь."

    bot.send_message(chat_id, history_text)


def log_expense(chat_id, amount):
    expense = {
        'date': datetime.today().strftime('%Y-%m-%d'),
        'amount': amount
    }
    if 'expenses' in user_data[chat_id]:
        user_data[chat_id]['expenses'].append(expense)
    else:
        user_data[chat_id]['expenses'] = [expense]


def ask_profession(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Какая ваша профессия?")
    bot.register_next_step_handler(msg, process_profession)


def process_profession(message):
    chat_id = message.chat.id
    user_data[chat_id]['profession'] = message.text
    ask_payday(message)


def ask_payday(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Какой ваш день выплаты зарплаты (число)?")
    bot.register_next_step_handler(msg, process_payday)


def process_payday(message):
    chat_id = message.chat.id
    user_data[chat_id]['payday'] = message.text
    ask_salary(message)


def ask_salary(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Какой ваш размер зарплаты?")
    bot.register_next_step_handler(msg, process_salary)


def process_salary(message):
    chat_id = message.chat.id
    user_data[chat_id]['salary'] = message.text
    bot.send_message(chat_id, "Спасибо за ответы! Опрос завершен.")
    show_main_menu(message)


def show_profile(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id, {})
    
    if user_info:
        profile_text = (
            "📋 Ваш профиль:\n"
            f"Профессия: {user_info.get('profession', 'Не указана')}\n"
            f"День выплаты зарплаты: {user_info.get('payday', 'Не указан')}\n"
            f"Размер зарплаты: {user_info.get('salary', 'Не указан')}\n"
        )
    else:
        profile_text = "Ваш профиль пуст. Пройдите опрос, чтобы заполнить его."

    bot.send_message(chat_id, profile_text)


@bot.message_handler(commands=['add_expense'])
def add_expense(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите сумму расхода:")
    bot.register_next_step_handler(message, process_add_expense)


def process_add_expense(message):
    chat_id = message.chat.id
    amount = message.text

    if amount.isdigit():
        log_expense(chat_id, amount)
        bot.send_message(chat_id, "Расход добавлен.")
    else:
        bot.send_message(chat_id, "Пожалуйста, введите корректную сумму.")


bot.polling()



