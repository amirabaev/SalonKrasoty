import telebot
from telebot import types
import re
from datetime import datetime

# ================ ТВОИ ДАННЫЕ (УЖЕ ВСТАВЛЕНЫ) ================
TOKEN = '8086852567:AAH77qUsDbu7RgwxVAHEDBOxMVAP2bLiBKg'
ADMIN_CHAT_ID = '6627729254'
# =============================================================

bot = telebot.TeleBot(TOKEN)
user_data = {}

# ================ КЛАВИАТУРЫ ================
def main_keyboard():
    """Главное меню"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = ["💇‍♀️ Услуги", "💰 Цены", "📝 Записаться", "📍 Контакты"]
    keyboard.add(*buttons)
    return keyboard

def phone_keyboard():
    """Клавиатура с кнопкой телефона"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("📱 Отправить номер телефона", request_contact=True)
    keyboard.add(button)
    return keyboard

def back_keyboard():
    """Клавиатура с кнопкой назад"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🔙 Назад в главное меню")
    return keyboard

# ================ ПРОВЕРКА НАЗАД ================
def check_back_button(message):
    """Проверяет, нажал ли пользователь кнопку назад"""
    if message.text == "🔙 Назад в главное меню":
        if message.chat.id in user_data:
            del user_data[message.chat.id]
        bot.send_message(
            message.chat.id,
            "🏠 Вы вернулись в главное меню",
            reply_markup=main_keyboard()
        )
        return True
    return False

# ================ СТАРТ ================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Приветствие"""
    user_name = message.from_user.first_name
    if message.chat.id in user_data:
        del user_data[message.chat.id]
    
    welcome_text = f"""
🌟 Добро пожаловать в салон красоты, {user_name}!

Я помогу вам:
• Ознакомиться с услугами и ценами
• Записаться на процедуру
• Узнать контакты и адрес

👇 Выберите нужный пункт в меню:
    """
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=main_keyboard()
    )

# ================ УСЛУГИ ================
@bot.message_handler(func=lambda message: message.text == "💇‍♀️ Услуги")
def services(message):
    """Список услуг"""
    if check_back_button(message):
        return
    
    text = """
💇‍♀️ *НАШИ УСЛУГИ:*

💆‍♀️ *ВОЛОСЫ:*
• Женские стрижки
• Мужские стрижки
• Окрашивание
• Ламинирование

💅 *НОГТИ:*
• Маникюр
• Педикюр
• Наращивание
• Дизайн ногтей

✨ *КОСМЕТОЛОГИЯ:*
• Чистка лица
• Массаж
• Уходовые процедуры
    """
    bot.send_message(
        message.chat.id,
        text,
        parse_mode='Markdown',
        reply_markup=back_keyboard()
    )

# ================ ЦЕНЫ ================
@bot.message_handler(func=lambda message: message.text == "💰 Цены")
def prices(message):
    """Прайс-лист"""
    if check_back_button(message):
        return
    
    text = """
💰 *ПРАЙС-ЛИСТ:*

💇‍♀️ *СТРИЖКИ:*
• Женская стрижка - 1500 ₽
• Мужская стрижка - 1000 ₽
• Укладка - 800 ₽

🎨 *ОКРАШИВАНИЕ:*
• Тонирование - от 2000 ₽
• Полное окрашивание - от 3500 ₽

💅 *МАНИКЮР:*
• Классический - 1500 ₽
• Аппаратный - 1700 ₽
• Гель-лак - +1000 ₽

💆‍♀️ *КОСМЕТОЛОГИЯ:*
• Чистка лица - 2500 ₽
• Массаж лица - 1500 ₽
    """
    bot.send_message(
        message.chat.id,
        text,
        parse_mode='Markdown',
        reply_markup=back_keyboard()
    )

# ================ КОНТАКТЫ ================
@bot.message_handler(func=lambda message: message.text == "📍 Контакты")
def contacts(message):
    """Контакты салона"""
    if check_back_button(message):
        return
    
    text = """
📍 *КАК НАС НАЙТИ:*

🏢 *АДРЕС:*
г. Москва, ул. Тверская, д. 15

⏰ *РЕЖИМ РАБОТЫ:*
Пн-Вс: 10:00 - 21:00

📞 *ТЕЛЕФОН:*
+7 (999) 123-45-67

🌐 *INSTAGRAM:*
@salon_krasoty
    """
    bot.send_message(
        message.chat.id,
        text,
        reply_markup=back_keyboard()
    )

# ================ ЗАПИСЬ ================
@bot.message_handler(func=lambda message: message.text == "📝 Записаться")
def start_booking(message):
    """Начало записи"""
    if check_back_button(message):
        return
    
    chat_id = message.chat.id
    user_data[chat_id] = {}
    
    text = """
📝 *ЗАПИСЬ НА ПРОЦЕДУРУ*

✏️ Напишите ваше имя:
    """
    bot.send_message(
        message.chat.id,
        text,
        parse_mode='Markdown',
        reply_markup=back_keyboard()
    )
    bot.register_next_step_handler(message, get_name)

# ================ ПОЛУЧЕНИЕ ИМЕНИ ================
def get_name(message):
    """Получает имя клиента"""
    chat_id = message.chat.id
    
    if check_back_button(message):
        return
    
    if message.text and message.text.strip():
        user_data[chat_id]['name'] = message.text.strip()
        
        text = """
📞 *УКАЖИТЕ НОМЕР ТЕЛЕФОНА*

Нажмите кнопку ниже 📱
или введите вручную:
+7 999 123-45-67
        """
        bot.send_message(
            message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=phone_keyboard()
        )
        bot.register_next_step_handler(message, get_phone)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Имя не может быть пустым. Введите имя:",
            reply_markup=back_keyboard()
        )
        bot.register_next_step_handler(message, get_name)

# ================ ПОЛУЧЕНИЕ ТЕЛЕФОНА ================
def get_phone(message):
    """Получает номер телефона"""
    chat_id = message.chat.id
    
    if check_back_button(message):
        return
    
    # Если отправил контакт
    if message.contact:
        phone = message.contact.phone_number
        user_data[chat_id]['phone'] = phone
        send_booking_to_admin(chat_id)
    
    # Если ввел вручную
    elif message.text:
        phone = re.sub(r'[^\d+]', '', message.text.strip())
        
        # Проверка номера
        if phone and (phone.startswith('+7') or phone.startswith('8') or phone.startswith('7')):
            if len(re.findall(r'\d', phone)) >= 10:
                if phone.startswith('8'):
                    phone = '+7' + phone[1:]
                elif phone.startswith('7') and not phone.startswith('+7'):
                    phone = '+7' + phone[1:]
                
                user_data[chat_id]['phone'] = phone
                send_booking_to_admin(chat_id)
            else:
                bot.send_message(
                    chat_id,
                    "❌ Слишком короткий номер. Введите полный номер:",
                    reply_markup=phone_keyboard()
                )
                bot.register_next_step_handler(message, get_phone)
        else:
            bot.send_message(
                chat_id,
                "❌ Неверный формат. Введите номер как +7XXXXXXXXXX",
                reply_markup=phone_keyboard()
            )
            bot.register_next_step_handler(message, get_phone)
    else:
        bot.send_message(
            chat_id,
            "❌ Отправьте номер телефона:",
            reply_markup=phone_keyboard()
        )
        bot.register_next_step_handler(message, get_phone)

# ================ ОТПРАВКА ЗАЯВКИ ================
def send_booking_to_admin(chat_id):
    """Отправляет заявку админу"""
    if chat_id not in user_data:
        return
    
    name = user_data[chat_id]['name']
    phone = user_data[chat_id]['phone']
    
    # Сообщение админу
    admin_message = f"""
🔔 НОВАЯ ЗАЯВКА!

👤 Имя: {name}
📱 Телефон: {phone}
📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
    """
    
    try:
        bot.send_message(ADMIN_CHAT_ID, admin_message)
        print(f"✅ Заявка от {name} отправлена админу")
    except Exception as e:
        print(f"⚠️ Ошибка отправки админу: {e}")
    
    # Сообщение клиенту
    thank_you_text = f"""
✅ *Спасибо, {name}!*

Ваша заявка принята! 📨
Мы свяжемся с вами по номеру:
📞 {phone}

В ближайшее время! 🌸
    """
    
    bot.send_message(
        chat_id,
        thank_you_text,
        parse_mode='Markdown',
        reply_markup=main_keyboard()
    )
    
    # Очищаем данные
    if chat_id in user_data:
        del user_data[chat_id]

# ================ НАЗАД ================
@bot.message_handler(func=lambda message: message.text == "🔙 Назад в главное меню")
def back_to_main(message):
    """Возврат в главное меню"""
    if message.chat.id in user_data:
        del user_data[message.chat.id]
    
    bot.send_message(
        message.chat.id,
        "🏠 Вы вернулись в главное меню",
        reply_markup=main_keyboard()
    )

# ================ ВСЁ ОСТАЛЬНОЕ ================
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    """Неизвестные команды"""
    bot.send_message(
        message.chat.id,
        "❓ Я вас не понимаю. Используйте кнопки меню 👇",
        reply_markup=main_keyboard()
    )

# ================ ЗАПУСК ================
if __name__ == '__main__':
    print("=" * 50)
    print("✅ БОТ САЛОНА КРАСОТЫ ЗАПУЩЕН!")
    print("=" * 50)
    print(f"🤖 Бот: @{bot.get_me().username}")
    print(f"👤 Админ ID: {ADMIN_CHAT_ID}")
    print("📱 Бот работает и ждет заявки!")
    print("=" * 50)
    print("🔴 НЕ ЗАКРЫВАЙ ЭТО ОКНО!")
    print("=" * 50)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            import time
            time.sleep(5)

