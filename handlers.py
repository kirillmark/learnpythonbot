from glob import glob
import os
from random import choice

from db import db, get_or_create_user
from utils import play_random_numbers, main_keyboard, has_object_on_image


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(
        f"Здравствуй, пользователь {user['emoji']}!",
        reply_markup=main_keyboard()
    )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    text = update.message.text
    update.message.reply_text(f"{text}{user['emoji']}",  reply_markup=main_keyboard())


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число!"
    else:
        message = "Введите число"
    update.message.reply_text(message,  reply_markup=main_keyboard())


def send_cat_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'),  reply_markup=main_keyboard())


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {user['emoji']}!",
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    photo_file.download(filename)
    update.message.reply_text("Файл сохранен")
    if has_object_on_image(filename, 'cat'):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, котик не обнаружен!")
