import logging
from for_email import send_email
from pyrogram import Client, filters
from keyboards import get_confirmation_keyboards, get_menu_keyboards
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)


app = Client(
    'YOUR BOT',
    bot_token='YOUR BOT TOKEN',
    api_id= 'YOUR API ID',
    api_hash='YOUR API HASH'
)


# Пишем Состояние State
STATE_WAITING_FOR_TITLE = "waiting_for_title"
STATE_CONFIRMING_TITLE = "confirming_title"
STATE_WAITING_FOR_MESSAGE = "waiting_for_message"
STATE_CONFIRMING_MESSAGE = "confirming_message"
STATE_WAITING_FOR_EMAIL = "waiting_for_email"
STATE_CONFIRMING_EMAIL = "confirming_email"

user_data = {}
user_settings = {}
user_states = {}


@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    chat_id = message.chat.id
    user_settings[chat_id] = {'notifications': True, 'language': 'Русский'}

    await message.reply(
        "👋Привет! Я бот для отслеживания изменений в чатах.\n"
        "🌟Авторы:\n"
        "- TG: [5ekastan](https://t.me/beka_stan)\n"
        "🚫Пока что бот не доступен для общего использования,\n"
        "но мы можем договориться о его использовании!",
        reply_markup=get_menu_keyboards()
    )

    

####################    НАСТРОЙКА       ########################
                                                            ####
@app.on_callback_query(filters.regex("settings"))             ###
async def settings_menu(client: Client, callback_query):       #############################
    settings_keyboard = InlineKeyboardMarkup([                                            ##
        [InlineKeyboardButton("🔔 Уведомления", callback_data="toggle_notifications")],   ##
        [InlineKeyboardButton("🌐 Язык", callback_data="change_language")],               ##
        [InlineKeyboardButton("🔄 Обновить профиль", callback_data="update_profile")]     ##
    ])                                                                  
                                                                        
    await callback_query.message.edit_text(                             
        "⚙️ *Настройки профиля:*\n\nВыберите настройку для изменения:", 
        reply_markup=settings_keyboard,                  
        one_time_keyboard=True,                          
        parse_mode="Markdown"                            
    )                                                    
                                                         
@app.on_callback_query(filters.regex("toggle_notifications|change_language|update_profile")) 
async def settings_callback(client: Client, callback_query):                            
    chat_id = callback_query.message.chat.id                                 
    data = callback_query.data                       
                                                    
    if chat_id not in user_settings:                 
        user_settings[chat_id] = {'notifications': True, 'language': 'Русский'}
                                                                               
    if data == "toggle_notifications":                                         
        current_status = user_settings[chat_id].get('notifications', True)                                                              
        user_settings[chat_id]['notifications'] = not current_status                                                                    
        status = "включены" if user_settings[chat_id]['notifications'] else "выключены"                                                 
        await callback_query.message.edit_text(f"🔔 Уведомления теперь {status}.", reply_markup=callback_query.message.reply_markup)   

    elif data == "change_language":
        current_language = user_settings[chat_id].get('language', 'Русский')
        new_language = 'English' if current_language == 'Русский' else 'Русский'
        user_settings[chat_id]['language'] = new_language
        await callback_query.message.edit_text(f"🌐 Язык изменен на {new_language}.", reply_markup=callback_query.message.reply_markup)

    elif data == "update_profile":
        await callback_query.message.edit_text(
            "🔄 Чтобы обновить профиль, используйте следующие команды:\n"
            "- Имя: /setname\n"
            "- Возраст: /setage\n"
            "- Город: /setcity",
            reply_markup=callback_query.message.reply_markup
        )

@app.on_message(filters.command("setname") & filters.private)
async def setname(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Пожалуйста, укажите имя после команды, например: `/setname Иван`")
        return
    name = args[1]
    user_data[message.chat.id] = {'name': name}
    await message.reply(f"Ваше имя обновлено на: {name}")

@app.on_message(filters.command("setage") & filters.private)
async def setage(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or not args[1].isdigit():
        await message.reply("Пожалуйста, укажите возраст числом, например: `/setage 25`")
        return
    age = int(args[1])
    user_data[message.chat.id] = user_data.get(message.chat.id, {})
    user_data[message.chat.id]['age'] = age
    await message.reply(f"Ваш возраст обновлен на: {age}")

@app.on_message(filters.command("setcity") & filters.private)
async def setcity(client: Client, message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:                                                                                   ##
        await message.reply("Пожалуйста, укажите город после команды, например: `/setcity Москва`")     ##
        return                                                                                          ##
    city = args[1]                                                      ##################################
    user_data[message.chat.id] = user_data.get(message.chat.id, {})    ###
    user_data[message.chat.id]['city'] = city                         ###
    await message.reply(f"Ваш город обновлен на: {city}")     ##########
                                                              ##
####################    НАСТРОЙКА       ########################


@app.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    help_text = (
        "🆘 *Как я могу помочь?*\n\n"
        "👋 Добро пожаловать! Я бот для отслеживания изменений в чатах и предоставляю следующие функции:\n\n"
        "*Основные команды:*\n"
        "/start - Запустить бота и открыть меню\n"
        "/reset - Сбросить текущий прогресс\n"
        "/help - Показать это сообщение с инструкциями\n\n"
        "*Кнопки меню:*\n"
        "📄 *Профиль* - Показать вашу информацию профиля (ID, Имя, Фамилия)\n"
        "📧 *Написать на почту* - Свяжитесь с нашей командой поддержки по почте\n"
        "📋 *Команды* - Список доступных команд для взаимодействия с ботом\n"
        "🔍 *Поиск* - В разработке (команда еще не доступна)\n"
        "📷 *Инстаграм* - Ссылка на наш Инстаграм-аккаунт\n"
        "🆘 *Помощь* - Это сообщение с описанием функций\n"
        "⚙️ *Настройки* - Настройка параметров профиля\n\n"
        "Если у вас возникли дополнительные вопросы, пожалуйста, напишите нам на почту\n\n"
        "🌟 Благодарим за использование нашего бота!"
    )
    await message.reply(help_text)
    

@app.on_message(filters.command("reset") & filters.private)
async def reset(client: Client, message: Message):
    chat_id = message.chat.id
    user_data.pop(chat_id, None)
    user_settings.pop(chat_id, None)
    user_states.pop(chat_id, None)
    await message.reply("Ваш прогресс был сброшен. Начните заново с командой /start")


@app.on_message(filters.text & filters.private)
async def profile(client: Client, message: Message):
    chat_id = message.chat.id
    
    if message.text == "Профиль":
        await message.reply(f"👤 Это ваш профиль:\n\nID: {message.from_user.id}\nИмя: {message.from_user.first_name}\nФамилия: {message.from_user.last_name}")

    elif message.text == "Написать на почту":
        await message.reply("📧 Почта 5ekastan\nНапишите тему письма.") 
        user_states[chat_id] = STATE_WAITING_FOR_TITLE

    # Обработка состояния ожидания темы письма
    elif user_states.get(chat_id) == STATE_WAITING_FOR_TITLE:
        user_states[f"{chat_id}_title"] = message.text  
        await message.reply("Все верно?",message.text, reply_markup=get_confirmation_keyboards())
        user_states[chat_id] = STATE_CONFIRMING_TITLE

    # Подтверждение темы письма
    elif user_states.get(chat_id) == STATE_CONFIRMING_TITLE:
        if message.text == "Да, все верно":
            await message.reply("Напишите текст письма.")
            user_states[chat_id] = STATE_WAITING_FOR_MESSAGE
        elif message.text == "Нет, изменить":
            await message.reply("Введите новую тему письма.")
            user_states[chat_id] = STATE_WAITING_FOR_TITLE
        else:
            await message.reply("Пожалуйста, выберите один из вариантов.", reply_markup=get_confirmation_keyboards())

    # Обработка состояния ожидания текста письма
    elif user_states.get(chat_id) == STATE_WAITING_FOR_MESSAGE:
        user_states[f"{chat_id}_message"] = message.text  
        await message.reply("Все верно?",message.text, reply_markup=get_confirmation_keyboards())
        user_states[chat_id] = STATE_CONFIRMING_MESSAGE

    # Подтверждение текста письма
    elif user_states.get(chat_id) == STATE_CONFIRMING_MESSAGE:
        if message.text == "Да, все верно":
            await message.reply("Введите email получателя.")
            user_states[chat_id] = STATE_WAITING_FOR_EMAIL
        elif message.text == "Нет, изменить":
            await message.reply("Введите новый текст письма.")
            user_states[chat_id] = STATE_WAITING_FOR_MESSAGE
        else:
            await message.reply("Пожалуйста, выберите один из вариантов.", reply_markup=get_confirmation_keyboards())
            
    elif user_states.get(chat_id) == STATE_WAITING_FOR_EMAIL:
        user_states[f"{chat_id}_email"] = message.text 
        title = user_states.get(f"{chat_id}_title", "Не указано")
        message_text = user_states.get(f"{chat_id}_message", "Не указано")
        email = message.text
        await message.reply(
            f"Получатель: {email}\nТема: {title}\nТекст: {message_text}\nВсе верно?",
            reply_markup=get_confirmation_keyboards()
        )
        user_states[chat_id] = STATE_CONFIRMING_EMAIL

    elif user_states.get(chat_id) == STATE_CONFIRMING_EMAIL:
            if message.text == "Да, все верно":
                await message.reply("Сообщение отправляется...")

                # Отправляем email
                email = user_states.get(f"{chat_id}_email")
                title = user_states.get(f"{chat_id}_title")
                message_text = user_states.get(f"{chat_id}_message")
                try:
                    send_email(email, title, message_text, image_path="./bekastan.png")
                    await message.reply("Сообщение отправлено.", reply_markup=get_menu_keyboards())
                    user_states.pop(chat_id, None)
                except Exception as e:
                    await message.reply(f"Ошибка при отправке сообщения: {e}", reply_markup=get_menu_keyboards())
                    user_states.pop(chat_id, None)
            elif message.text == "Нет, изменить":
                await message.reply("Введите новый email получателя.")
                user_states[chat_id] = STATE_WAITING_FOR_EMAIL
            else:
                await message.reply("Пожалуйста, выберите один из вариантов.", reply_markup=get_confirmation_keyboards())



    elif message.text == "Команды":
        await message.reply("📋 Доступные команды:\n/start - Запуск бота\n/reset - Сбросить прогресс\n/help - Помощь\n")

    elif message.text == "Поиск":
        await message.reply("Не понял что делать для это команды.")

    elif message.text == "Инстаграм":
        await message.reply("📷 Наш Инстаграм: [5ekastan](https://instagram.com/5ekastan)", disable_web_page_preview=True)

    elif message.text == "Помощь":
        await message.reply("🆘 Как я могу помочь?\nЕсли у вас возникли вопросы, используйте команду /help или свяжитесь с нами по почте.")

    elif message.text == "Настройки":
        settings_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔔 Уведомления", callback_data="toggle_notifications")],
            [InlineKeyboardButton("🌐 Язык", callback_data="change_language")],
            [InlineKeyboardButton("🔄 Обновить профиль", callback_data="update_profile")]
        ])
        
        await message.reply(
            "⚙️ *Настройки профиля:*\n\nВыберите настройку для изменения:",
            reply_markup=settings_keyboard,
        )
    else:
        await message.reply("Пожалуйста, Выберите команды из меню.", reply_markup=get_menu_keyboards())


app.run()