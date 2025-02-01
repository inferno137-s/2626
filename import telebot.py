import telebot
from telebot import types

bot = telebot.TeleBot('7677815065:AAHAJOUVybTC2VnUiK41dr9X7A3fl7NKmXE')

# States
STATE_PROFESSION = 0
STATE_PAYDAY = 1
STATE_SALARY = 2
STATE_FINISHED = 3

user_data = {} # Хранит данные пользователя


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "🎉 Привет! Добро пожаловать в наш бот где ты сможешь считать свой бюджет!")
    show_main_menu(message)


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Опрос"), types.KeyboardButton("Меню"))
    bot.send_message(message.chat.id, "Вы в главном меню. Выберите опцию:", reply_markup=markup)


def show_powerlifting_options(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "Мои деньги",
        "История",
        "Календарь",
        "Ежедневной нормы расходов",
        "Советы",
        "🔙 Назад"
    ]
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    bot.send_message(message.chat.id, "Выберите одну из тем:", reply_markup=markup)


def send_excel_file(message):
    files = {
        "Мои деньги": 'D:\\TelegramBot\\BOT\\BBB\\Пауэр\\Начальный.xlsx',
        "История": 'D:\\TelegramBot\\BOT\\BBB\\Пауэр\\Средний.xlsx',
        "Календарь": 'D:\\TelegramBot\\BOT\\BBB\\Пауэр\\Высокий.xlsx',
        "Ежедневной нормы расходов": 'D:\\TelegramBot\\BOT\\BBB\\Пауэр\\Жимовые раскладки.docx',
        "Советы": 'D:\\TelegramBot\\BOT\\BBB\\Пауэр\\Жимовые раскладки.docx'
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
        elif message.text in ["Мои деньги", "История", "Календарь", "Ежедневной нормы расходов", "Советы"]:
            send_excel_file(message)
        elif message.text == "🔙 Назад":
            show_main_menu(message)
        elif message.text == "Опрос":
            user_data[chat_id] = {} # Инициализация данных пользователя
            ask_profession(message)


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
    msg = bot.send_message(chat_id, "Когда вы получаете зарплату? (например, 10 числа)")
    bot.register_next_step_handler(msg, process_payday)


def process_payday(message):
    chat_id = message.chat.id
    user_data[chat_id]['payday'] = message.text
    ask_salary(message)


def ask_salary(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Какая ваша зарплата? (число)")
    bot.register_next_step_handler(msg, process_salary)


def process_salary(message):
    chat_id = message.chat.id
    try:
        salary = int(message.text)
        user_data[chat_id]['salary'] = salary
        bot.send_message(chat_id, f"Спасибо! Ваши данные:\nПрофессия: {user_data[chat_id]['profession']}\nДата зарплаты: {user_data[chat_id]['payday']}\nЗарплата: {user_data[chat_id]['salary']}")
        show_main_menu(message) # Возвращаемся в главное меню после завершения опроса

    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите число для зарплаты.")
        ask_salary(message) # Повторяем вопрос, если ввод некорректный


bot.polling()

