from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton 

def get_confirmation_keyboards():
    true_button = KeyboardButton("Да, все верно")
    false_button = KeyboardButton("Нет, изменить")
    keyboard = ReplyKeyboardMarkup(
        [[true_button, false_button]],
          resize_keyboard=True,
          one_time_keyboard=True
    )
    return keyboard


def get_menu_keyboards():
    profile_button = KeyboardButton("Профиль")
    email_button = KeyboardButton("Написать на почту")
    comands_button = KeyboardButton("Команды")
    search_button = KeyboardButton("Поиск")
    instagram_button = KeyboardButton("Инстаграм")
    help_button = KeyboardButton("Помощь")
    settings_button = KeyboardButton("Настройки")
    
    keyboard = ReplyKeyboardMarkup(
        [[profile_button, email_button],
         [comands_button, search_button],
         [instagram_button, help_button],
         [settings_button]],
        resize_keyboard=True
    )

    return keyboard
