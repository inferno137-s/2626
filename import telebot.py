import telebot
from telebot import types
from datetime import datetime, timedelta
import schedule
import time
import threading
import random

bot = telebot.TeleBot("7677815065:AAHAJOUVybTC2VnUiK41dr9X7A3fl7NKmXE")

user_data = {}

categories = ["Еда", "Транспорт", "Развлечения", "Жилье", "Другое"]

advice_list = [
    "Создайте бюджет и строго следуйте ему.",
    "Откладывайте 10% от каждой зарплаты.",
    "Используйте приложения для учета расходов.",
    "Избегайте импульсивных покупок.",
    "Планируйте крупные покупки заранее.",
    "Инвестируйте в свое образование.",
    "Сравнивайте цены перед покупкой.",
    "Используйте кэшбэк-сервисы.",
    "Регулярно проверяйте свои финансовые цели.",
    "Избегайте долгов с высокими процентами.",
    "Создайте подушку безопасности на 3-6 месяцев.",
    "Используйте автоматические переводы на сберегательный счет.",
    "Покупайте товары в сезон распродаж.",
    "Не берите кредиты на развлечения.",
    "Регулярно анализируйте свои расходы.",
    "Используйте правило 50/30/20: 50% на нужды, 30% на желания, 20% на сбережения.",
    "Не храните все деньги на одной карте.",
    "Изучайте основы финансовой грамотности.",
    "Планируйте пенсионные накопления.",
    "Избегайте ненужных подписок.",
]

def send_notifications():
    while True:
        schedule.run_pending()
        time.sleep(1)

notification_thread = threading.Thread(target=send_notifications)
notification_thread.daemon = True
notification_thread.start()

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "🎉 Привет! Добро пожаловать в наш финансовый бот!")
    show_main_menu(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Личные данные", "Расходы", "Календарь", "Профиль", "Норма расходов", "Удалить расход", "Советы"]
    markup.add(*[types.KeyboardButton(btn) for btn in buttons])
    bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Личные данные":
        survey(message)
    elif message.text == "Расходы":
        add_expense(message)
    elif message.text == "Календарь":
        handle_calendar(message)
    elif message.text == "Профиль":
        show_profile(message)
    elif message.text == "Норма расходов":
        show_expense_norm(message)
    elif message.text == "Удалить расход":
        delete_last_expense(message)
    elif message.text == "Советы":
        send_random_advice(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите опцию из меню.")

def send_random_advice(message):
    chat_id = message.chat.id
    random_advice = random.choice(advice_list)
    bot.send_message(chat_id, f"💡 Совет дня:\n\n{random_advice}")

def survey(message):
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, save_name)

def save_name(message):
    chat_id = message.chat.id
    name = message.text.strip()
    
    if name:
        user_data[chat_id] = {'name': name, 'expenses': []}
        bot.send_message(chat_id, "Введите место работы:")
        bot.register_next_step_handler(message, save_workplace)
    else:
        bot.send_message(chat_id, "Имя не может быть пустым, попробуйте снова.")
        survey(message)

def save_workplace(message):
    chat_id = message.chat.id
    workplace = message.text.strip()
    
    if workplace:
        user_data[chat_id]['workplace'] = workplace
        bot.send_message(chat_id, "Введите свою зарплату:")
        bot.register_next_step_handler(message, save_salary)
    else:
        bot.send_message(chat_id, "Место работы не может быть пустым, попробуйте снова.")
        save_workplace(message)

def save_salary(message):
    chat_id = message.chat.id
    try:
        salary = float(message.text)
        user_data[chat_id]['salary'] = salary
        bot.send_message(chat_id, "Введите число аванса (только день, например, 15):")
        bot.register_next_step_handler(message, save_advance_date)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное число.")
        save_salary(message)

def save_advance_date(message):
    chat_id = message.chat.id
    try:
        day = int(message.text.strip())
        today = datetime.now()
        advance_date = today.replace(day=day).date()
        
        if advance_date < today.date():
            advance_date = advance_date.replace(month=today.month + 1)
        
        user_data[chat_id]['advance_date'] = advance_date
        bot.send_message(chat_id, "Введите число зарплаты (только день, например, 30):")
        bot.register_next_step_handler(message, save_salary_date)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное число.")
        save_advance_date(message)

def save_salary_date(message):
    chat_id = message.chat.id
    try:
        day = int(message.text.strip())
        today = datetime.now()
        salary_date = today.replace(day=day).date()
        
        if salary_date < today.date():
            salary_date = salary_date.replace(month=today.month + 1)
        
        user_data[chat_id]['salary_date'] = salary_date
        
        
        if 'name' in user_data[chat_id] and 'workplace' in user_data[chat_id] and 'salary' in user_data[chat_id] and 'advance_date' in user_data[chat_id] and 'salary_date' in user_data[chat_id]:
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Расходы", "Календарь", "Профиль", "Норма расходов", "Удалить расход", "Советы"]
            markup.add(*[types.KeyboardButton(btn) for btn in buttons])
            
            bot.send_message(chat_id, "Ваши данные сохранены! Возвращайтесь в главное меню.", reply_markup=markup)
            setup_notifications(chat_id)
        else:
            bot.send_message(chat_id, "Что-то пошло не так. Попробуйте снова.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное число.")
        save_salary_date(message)

def add_expense(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[types.KeyboardButton(category) for category in categories])
    bot.send_message(chat_id, "Выберите категорию расхода:", reply_markup=markup)
    bot.register_next_step_handler(message, save_expense_category)

def save_expense_category(message):
    chat_id = message.chat.id
    category = message.text.strip()
    
    if category in categories:
        user_data[chat_id]['current_category'] = category
        bot.send_message(chat_id, "Введите сумму расхода:")
        bot.register_next_step_handler(message, save_expense_amount)
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите категорию из списка.")
        add_expense(message)

def save_expense_amount(message):
    chat_id = message.chat.id
    try:
        expense_amount = float(message.text)
        category = user_data[chat_id]['current_category']
        
        if 'expenses' not in user_data[chat_id]:
            user_data[chat_id]['expenses'] = []
        
        user_data[chat_id]['expenses'].append({
            'amount': expense_amount,
            'category': category,
            'date': datetime.now().strftime("%d.%m.%Y %H:%M")
        })
        
        bot.send_message(chat_id, f"Расход добавлен: {expense_amount} у.е. (категория: {category}).")
        show_main_menu(message)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное число.")
        save_expense_amount(message)

def delete_last_expense(message):
    chat_id = message.chat.id
    if 'expenses' in user_data.get(chat_id, {}) and user_data[chat_id]['expenses']:
        last_expense = user_data[chat_id]['expenses'].pop()
        bot.send_message(chat_id, f"Последний расход удален: {last_expense['amount']} у.е. (категория: {last_expense['category']}).")
    else:
        bot.send_message(chat_id, "Нет расходов для удаления.")
    show_main_menu(message)

def show_profile(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id)
    
    if user_info:
        expenses = user_info.get('expenses', [])
        total_expenses = sum(expense['amount'] for expense in expenses)
        
        profile_info = (
            f"👤 Имя: {user_info.get('name')}\n"
            f"🏢 Место работы: {user_info.get('workplace')}\n"
            f"💰 Зарплата: {user_info.get('salary', 'Не указана')} у.е.\n"
            f"📅 Дата аванса: {user_info.get('advance_date', 'Не указана')}\n"
            f"📅 Дата зарплаты: {user_info.get('salary_date', 'Не указана')}\n"
            f"💸 Общие расходы: {total_expenses} у.е.\n"
            f"📊 Расходы по категориям:\n"
        )
        category_expenses = {}
        for expense in expenses:
            category = expense['category']
            if category not in category_expenses:
                category_expenses[category] = 0
            category_expenses[category] += expense['amount']
        
        for category, amount in category_expenses.items():
            profile_info += f"  - {category}: {amount} у.е.\n"
        
        bot.send_message(chat_id, profile_info)
    else:
        bot.send_message(chat_id, "Сначала введите свои данные в личные данные.")

def show_expense_norm(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id)

    if user_info:
        salary = user_info.get('salary', 0)
        expenses = sum(expense['amount'] for expense in user_info.get('expenses', []))
        remaining_money = salary - expenses

        if remaining_money > 0:
            days_until_salary = (user_info.get('salary_date') - datetime.now().date()).days
            if days_until_salary > 0:
                daily_expense_limit = remaining_money / days_until_salary
            else:
                daily_expense_limit = 0

            emergency_fund = salary * 0.1

            norm_message = (
                f"💵 Осталось денег: {remaining_money:.2f} у.е.\n"
                f"📅 Денег можно потратить за день: {daily_expense_limit:.2f} у.е.\n"
                f"💼 Резерв на крайний случай: {emergency_fund:.2f} у.е."
            )
            bot.send_message(chat_id, norm_message)
        else:
            bot.send_message(chat_id, "У вас нет оставшихся средств. Пожалуйста, пересмотрите ваши расходы.")
    else:
        bot.send_message(chat_id, "Сначала введите свои данные в личные данные.")

def handle_calendar(message):
    chat_id = message.chat.id
    user_info = user_data.get(chat_id)
    
    if user_info:
        today = datetime.now().date()
        salary_date = user_info.get('salary_date')
        advance_date = user_info.get('advance_date')
        
        response = ""
        
        if salary_date:
            days_until_salary = (salary_date - today).days
            response += f"👷 До следующей зарплаты осталось: {days_until_salary} дней.\n"
        if advance_date:
            days_until_advance = (advance_date - today).days
            response += f"💰 До следующего аванса осталось: {days_until_advance} дней."     
        bot.send_message(chat_id, response or "Нет информации о зарплате или авансе.")
    else:
        bot.send_message(chat_id, "Сначала введите свои данные в личные данные.")

def setup_notifications(chat_id):
    user_info = user_data.get(chat_id)
    if user_info:
        salary_date = user_info.get('salary_date')
        advance_date = user_info.get('advance_date')
        
        if salary_date:
            schedule.every().day.at("09:00").do(
                lambda: bot.send_message(chat_id, "Завтра зарплата! 🎉")
            ).tag(str(chat_id))
        
        if advance_date:
            schedule.every().day.at("09:00").do(
                lambda: bot.send_message(chat_id, "Завтра аванс! 💰")
            ).tag(str(chat_id))

bot.polling(none_stop=True)
