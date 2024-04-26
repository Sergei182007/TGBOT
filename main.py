import telebot
import sqlite3
from telebot import types
from datetime import datetime
import random
import re
import requests
import json
from num2words import num2words

bot = telebot.TeleBot('6717203066:AAFTeOlXXp22qUyOcCm7AznOuMu5ruMEjl0')
api_key = "d5266e93-d944-4940-81bc-3f5ebe29776b"

morning = ['Доброе утро! Чем я могу Вам помочь?', "Доброе утро! Что пожелаете?",
           'Доброе утро! Чем я могу быть Вам полезен?']
afterning = ['Добрый день! Чем я могу Вам помочь?', "Добрый день! Что пожелаете?",
             'Добрый день! Чем я могу быть Вам полезен?']
evening = ['Добрый вечер! Чем я могу Вам помочь?', "Добрый вечер! Что пожелаете?",
           'Добрый вечер! Чем я могу быть Вам полезен?']
night = ['Доброй ночи! Чем я могу Вам помочь?', "Доброй ночи! Что пожелаете?",
         'Доброй ночи! Чем я могу быть Вам полезен?']

sp = []
bro = {}
users = {}

plays = {}



@bot.message_handler(commands=['start'])
def starts(message):
    markup = types.InlineKeyboardMarkup()
    plays[f"{str(message.from_user.id)}"] = 0
    bro[f"{str(message.from_user.id)}"] = []
    print(bro)
    # добавляем на нее две кнопки
    button2 = types.InlineKeyboardButton(text="🍽 Забронировать столик", callback_data="broni")
    button3 = types.InlineKeyboardButton(text="5️ Оставить отзыв",
                                         url="https://docs.google.com/forms/d/e/1FAIpQLSfXVkqmB07eV1GkmOPNBSReLkNvan8V1Cr4i8INLRHab0JrbQ/viewform")
    button4 = types.InlineKeyboardButton(text="🚕️ Где нас найти?", callback_data="address")
    button5 = types.InlineKeyboardButton(text="❓️ Задать вопрос", callback_data="question")
    button6 = types.InlineKeyboardButton(text="Как получить скидку", callback_data="playplay")
    markup.add(button2)
    markup.add(button3)
    markup.row(button4, button5)
    markup.add(button6)
    current_time = datetime.now()
    if current_time.hour in [5, 6, 7, 8, 9, 10, 11]:
        bot.send_message(message.chat.id, random.choice(morning), reply_markup=markup)
    elif current_time.hour in [12, 13, 14, 15, 16]:
        bot.send_message(message.chat.id, random.choice(afterning), reply_markup=markup)
    elif current_time.hour in [17, 18, 19, 20, 21]:
        bot.send_message(message.chat.id, random.choice(evening), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, random.choice(night), reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message, page=1, previous_message=None):
    connect = sqlite3.connect("menu")
    cursor = connect.cursor()

    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM dishes").fetchall()
    pages_count = str(pages_count_query[0])

    product_query = cursor.execute(f"SELECT title, description, photo, price FROM dishes WHERE page = ?;",
                                   (page,))
    title, description, photo, price = product_query.fetchone()

    buttons = types.InlineKeyboardMarkup()
    if page != 1:
        left = page - 1
    else:
        left = 7
    if page != 7:
        right = page + 1
    else:
        right = 1

    left_button = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button = types.InlineKeyboardButton(f"{str(page)}/{str(pages_count)[1:2]}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buy_button = types.InlineKeyboardButton("КУПИТЬ", callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(buy_button)

    try:
        try:
            pho = open(photo, 'rb')
        except:
            pho = photo
        msg = f"Название: {title}\nОписание: "
        msg += f"{description}\n"
        msg += f"Цена: {price} рублей\n"

        bot.send_photo(message.chat.id, photo=pho, caption=msg, reply_markup=buttons)
    except:
        msg = f"Название: {title}\nОписание: "
        msg += f"{description}\n"
        msg += f"Цена: {price} рублей\n"

        bot.send_message(message.chat.id, msg, reply_markup=buttons)
    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except:
        pass


@bot.message_handler(commands=['play'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    k = types.InlineKeyboardButton(text="🗿", callback_data="🗿")
    g = types.InlineKeyboardButton(text="✂️", callback_data="✂️")
    b = types.InlineKeyboardButton(text="📄", callback_data="📄")

    markup.add(k, g, b)
    bot.send_message(message.chat.id, "Выберите один из предметов: ", reply_markup=markup)


def play(message):
    markup = types.InlineKeyboardMarkup()
    k = types.InlineKeyboardButton(text="🗿", callback_data="🗿")
    g = types.InlineKeyboardButton(text="✂️", callback_data="✂️")
    b = types.InlineKeyboardButton(text="📄", callback_data="📄")

    markup.add(k, g, b)
    bot.send_message(message.chat.id, "Выберите один из предметов: ", reply_markup=markup)


def handle_text(message):
    bot.send_location(message.chat.id, 60.94549942, 76.590583801)


@bot.message_handler(commands=['br'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, '👨‍👩‍👦‍👦 Сколько человек пойдет с Вами?')
    bot.register_next_step_handler(message, first)


def first(message):
    name = message.text
    chat_id = message.chat.id
    buttonfirst = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("⬅️ Назад", callback_data='12345')
    buttonfirst.add(btn1)
    if int(name) > 10:
        bot.send_message(chat_id, "К сожалению, забронировать столик можно не более чем для 10 человек")
    else:
        bro[f"{str(message.from_user.id)}"].append(name)
        bot.send_message(chat_id, '📆 Укажите дату, на которую бы Вы хотели забронировать столик',
                         reply_markup=buttonfirst)
    bot.register_next_step_handler(message, second)


def second(message):
    chat_id = message.chat.id
    name = message.text
    buttonsecond = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("⬅️ Назад", callback_data='12345')
    buttonsecond.add(btn1)
    bro[f"{str(message.from_user.id)}"].append(name)
    bot.send_message(chat_id, f'⌚️ Отлично! Теперь укажите время, на которое Вы хотите забронировать столик',
                     reply_markup=buttonsecond)
    bot.register_next_step_handler(message, third)


def third(message):
    chat_id = message.chat.id
    name = message.text
    buttonthird = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("⬅️ Назад", callback_data='12345')
    buttonthird.add(btn1)
    bro[str(message.from_user.id)].append(name)
    bot.send_message(chat_id, f'Отлично! Теперь укажите дополнительные пожелания, если они есть',
                     reply_markup=buttonthird)
    bot.register_next_step_handler(message, four)


def four(message):
    chat_id = message.chat.id
    name = message.text
    fourth = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("⬅️ Назад", callback_data='12345')
    fourth.add(btn1)
    if "Номер телефона введен неверно" not in name:
        bro[str(message.from_user.id)].append(name)
        bot.send_message(chat_id, f'Супер! Осталось указать номер телефона, чтобы мы могли с Вами связаться',
                         reply_markup=fourth)
    else:
        bot.send_message(chat_id, f'Введите номер телефона ещё раз.')
    bot.register_next_step_handler(message, five)


def five(message):
    global bro
    name = message.text
    result = re.match(r"^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$", name)
    if result:
        bro[str(message.from_user.id)].append(name)
        print(bro)
        button = types.InlineKeyboardMarkup()
        no = types.InlineKeyboardButton("❌ Отменить", callback_data='no')
        yes = types.InlineKeyboardButton("✅ Подтвердить", callback_data='yes')
        button.add(no)
        button.add(yes)
        chat_id = message.chat.id
        surname = message.text
        bro[str(message.from_user.id)].append(surname)
        bot.send_message(chat_id, f'''Ваши данные успешно сохранены! Проверьте заказ: 
    Количество человек: {bro[str(message.from_user.id)][0]}
    Время: {bro[str(message.from_user.id)][1]}  {bro[str(message.from_user.id)][2]}
    Доп пожелания: {bro[str(message.from_user.id)][3]}''', reply_markup=button)
    else:
        buttons = types.InlineKeyboardMarkup()
        reset = types.InlineKeyboardButton("Ввести ещё раз", callback_data='reset')
        helpmenu = types.InlineKeyboardButton("Вернуться в меню", callback_data='menuuu')
        buttons.add(reset)
        buttons.add(helpmenu)
        bot.send_message(message.chat.id, 'Номер телефона введен неверно', reply_markup=buttons)


def send_chef(message):
    bot.send_message(1970887100, message)


def question(message):
    current = datetime.now()
    if int(current.hour) in [6, 7, 8, 9, 10, 11]:
        bot.send_message(message.chat.id,
                         f"Доброе утро! Вы можете задать нам вопрос, мы постараемся на него ответить".format(
                             message.from_user,
                             bot.get_me()),
                         parse_mode='html')
    elif int(current.hour) in [12, 13, 14, 15, 16]:
        bot.send_message(message.chat.id,
                         f"Добрый день! Вы можете задать нам вопрос, мы постараемся на него ответить".format(
                             message.from_user,
                             bot.get_me()),
                         parse_mode='html')

    # bot.send_message(chat_id="6361272148", text=f"Присоединился пользователь {message.from_user.first_name}")
    elif int(current.hour) in [17, 18, 19, 20, 21]:
        bot.send_message(message.chat.id,
                         f"Добрый вечер! Вы можете задать нам вопрос, мы постараемся на него ответить".format(
                             message.from_user,
                             bot.get_me()),
                         parse_mode='html')
    else:
        bot.send_message(message.chat.id,
                         f"Доброй ночи! Вы можете задать нам вопрос, мы постараемся на него ответить".format(
                             message.from_user,
                             bot.get_me()),
                         parse_mode='html')
    bot.register_next_step_handler(message, help_bot)


def help_bot(message):
    sp.append((message.message_id, message.chat.id))
    bot.forward_message(1970887100, message.chat.id, message.message_id)
    markup_inline = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{message.chat.id}')
    ], [
        types.InlineKeyboardButton(text='Отклонить', callback_data=f'delete{message.chat.id}')
    ]])
    bot.send_message(1970887100, f"Действие:", reply_markup=markup_inline)
    bot.register_next_step_handler(message, help_bot)


@bot.message_handler(commands=["requests"], func=lambda m: int(m.chat.id) == int(1970887100))
def all_messages(message):
    bot.send_message(message.chat.id, "Доступные запросы:")
    for i, req in enumerate(sp):
        bot.forward_message(1970887100, req[1], req[0])
        markup_inline = types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{message.chat.id}')
        ], [
            types.InlineKeyboardButton(text='Отклонить', callback_data=f'delete{message.chat.id}')
        ]])
        bot.send_message(message.chat.id, f"Действие:", reply_markup=markup_inline)


def send_answer(message: types.Message, call, chat_id):
    bot.send_message(call.message.chat.id, "Ответ отправлен!")
    bot.send_message(chat_id, message.text)
    for i, req in enumerate(sp):
        if int(req[1]) == int(chat_id):
            del sp[i]


@bot.callback_query_handler(func=lambda call: True)
def function(call):
    global bro
    if call.data == "address":
        bot.register_next_step_handler(call.message, handle_text(message=call.message))
    if 'to' in call.data:
        page = int(call.data.split(' ')[1])
        menu(call.message, page=page, previous_message=call.message)
    if call.data == "question":
        question(message=call.message)
    if call.data == "broni":
        welcome(message=call.message)
    if call.data == "reset":
        four(message=call.message)
    if call.data.startswith("answer"):
        chat_id = int(call.data[6:])
        bot.send_message(call.message.chat.id, "Напишите ответное сообщение пользователю")
        bot.register_next_step_handler(call.message, lambda msg: send_answer(msg, call, chat_id))
    if call.data.startswith("delete"):
        chat_id = int(call.data[6:])
        bot.send_message(chat_id, "Администратор посчитал Ваш запрос плохим")
    if call.data == "no":
        bot.send_message(call.message.chat.id,
                         'Вы отменили бронирование столика, но можете попробовать еще раз. Напишите /br')
        bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "playplay":
        play(message=call.message)
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Ваш заказ успешно отправлен!')
        bot.delete_message(call.message.chat.id, call.message.message_id)
        send_chef(message=f"""Новый заказ:
Количество: {bro[str(call.from_user.id)][0]} 
Время: {bro[str(call.from_user.id)][1]}  {bro[str(call.from_user.id)][2]}
Доп пожелания: {bro[str(call.from_user.id)][3]}
Телефон: {bro[str(call.from_user.id)][4]}""")
        bro[str(call.from_user.id)] = []

    if call.data == "12345":
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bro[str(call.message.chat.id)] = []
        starts(message=call.message)
        bot.delete_message(call.message.chat.id, call.message.message_id)

    playing_sp = ['🗿', '✂️', '📄']
    choice = random.choice(playing_sp)

    if call.data == '🗿':
        bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы выбрали: 🗿 Камень", reply_markup=None)

    elif call.data == '✂️':
        bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы выбрали: ✂️ Ножницы", reply_markup=None)
    elif call.data == '📄':
        bot.answer_callback_query(callback_query_id=call.id, text='Ваш ход принят!')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы выбрали: 📄 Бумагу", reply_markup=None)

    if call.data == choice:
        bot.send_message(call.message.chat.id,
                         f"У вас ничья! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")

    elif call.data == "🗿":
        if choice == "✂️":
            bot.send_message(call.message.chat.id,
                             f"Вы победили! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")
            plays[str(call.from_user.id)] += 1
            t = num2words(plays[str(call.from_user.id)], lang="ru", to="ordinal")
            bot.send_message(call.message.chat.id, f"Поздравляем, Вы выиграли у бота {t} раз")
            if t == "десятый":
                bot.send_message(call.message.chat.id,
                                 f"Поздравляем, Вы получили скидку {random.choice([1, 2, 4, 5])}%")
                plays[str(call.from_user.id)] = 0

        else:
            bot.send_message(call.message.chat.id,
                             f"Вы проиграли! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")

    elif call.data == "📄":
        if choice == "🗿":
            bot.send_message(call.message.chat.id,
                             f"Вы победили! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")
            plays[str(call.from_user.id)] += 1
            t = num2words(plays[str(call.from_user.id)], lang="ru", to="ordinal")
            bot.send_message(call.message.chat.id, f"Поздравляем, Вы выиграли у бота {t} раз")
            if t == "десятый":
                bot.send_message(call.message.chat.id,
                                 f"Поздравляем, Вы получили скидку {random.choice([1, 2, 4, 5])}%!")
                plays[str(call.from_user.id)] = 0

        else:
            bot.send_message(call.message.chat.id,
                             f"Вы проиграли! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")

    elif call.data == "✂️":
        if choice == "📄":
            bot.send_message(call.message.chat.id,
                             f"Вы победили! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")
            plays[str(call.from_user.id)] += 1
            t = num2words(plays[str(call.from_user.id)], lang="ru", to="ordinal")
            bot.send_message(call.message.chat.id, f"Поздравляем, Вы выиграли у бота {t} раз!")
            if t == "десятый":
                bot.send_message(call.message.chat.id,
                                 f"Поздравляем, Вы получили скидку {random.choice([1, 2, 4, 5])}%!!")
                plays[str(call.from_user.id)] = 0

        else:
            bot.send_message(call.message.chat.id,
                             f"Вы проиграли! Бот выбрал: {choice}\n\nЧтобы начать новую игру напишите: /play")


bot.polling(none_stop=True)
