# -*- coding: utf-8 -*-
import telebot, sqlite3
from telebot import *
import time

bot = telebot.TeleBot('878479849:AAE6JYUMCYfslkFC_ZOGsh9SQCx3BXL3tTQ')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    con = sqlite3.connect('UCK.sqlite3')
    cur = con.cursor()
    cid = message.chat.id
    nick = message.from_user.first_name
    mt = message.text
    main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_buttons.add('Мои данные', 'О нас', 'Оборудование')
    main_buttons.add('Галерея', 'Контакты', 'Сотрудники')
    ids = []
    for row in cur.execute('SELECT * FROM telegram_users'):
        ids.append(str(row[1]))
    if str(cid) in ids:
        for row in cur.execute(f'SELECT * FROM telegram_users WHERE message_chat_id = {cid}'):
            bot.send_message(cid, f'С возвращением, {row[3]} {row[4]}', reply_markup=main_buttons)
        working(message)
    elif str(cid) not in ids:
        registration(message)

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def registration(message):
    con = sqlite3.connect('UCK.sqlite3')
    cur = con.cursor()
    cid = message.chat.id
    nick = message.from_user.first_name
    mt = message.text
    mt = mt.capitalize()
    ids = []
    main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_buttons.add('Мои данные', 'О нас', 'Оборудование')
    main_buttons.add('Галерея', 'Контакты', 'Сотрудники')
    reg = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    reg.add('Регистрация')
    for row in cur.execute('SELECT * FROM telegram_users'):
        ids.append(str(row[1]))
    if str(cid) not in ids:
        if mt == '/start':
            bot.send_message(cid, 'Похоже Вы не зарегистрированы. Нажмите кнопку "Регистрация", чтобы начать пользоваться ботом', reply_markup=reg)
        if mt == 'Регистрация':
            bot.send_message(cid, 'Напишите свои ФИО через "_".\nПример: Нурпеисов_Ербол_Мендыбаевич')
        elif '_' in mt:
            fio = mt.split('_')
            name_count = 0
            for i in fio:
                name_count += 1
            if name_count == 3:
                fam = fio[0].capitalize()
                name = fio[1].capitalize()
                otch = fio[2].capitalize()
            elif name_count == 2:
                fam = fio[0].capitalize()
                name = fio[1].capitalize()
                otch = ''
            else:
                bot.send_message(cid, 'Напишите свои ФИО через "_".\nПример: Нурпеисов_Ербол_Мендыбаевич\nБудьте внимательны!')
            cur.execute('INSERT INTO telegram_users (message_chat_id, Fam, Name, Otch, Nickname) VALUES (?, ?, ?, ?, ?)', (cid, fam, name, otch, nick))
            con.commit()
            for row in cur.execute('SELECT * FROM telegram_users'):
                ids.append(str(row[1]))
            if str(cid) not in ids:
                registartion(message)
            else:
                bot.send_message(cid, 'Поздравляю! Вы зарегистрированы.', reply_markup=main_buttons)
                bot.send_message(888833912, f'Новый пользователь: {cid}/{nick} {fam} {name} {otch}')
                working(message)

    elif str(cid) in ids:
        working(message)

def working(message):
    con = sqlite3.connect('UCK.sqlite3')
    cur = con.cursor()
    cid = message.chat.id
    nick = message.from_user.first_name
    mt = message.text
    mt = mt.capitalize()
    main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_buttons.add('Мои данные', 'О нас', 'Оборудование')
    main_buttons.add('Галерея', 'Контакты', 'Сотрудники')
    back_to_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_main.add('Назад')
    logo_original = 'https://psv4.userapi.com/c856224/u232799244/docs/d8/ba8ba5cf0adb/logo_original.png?extra=7-u5wDzEK1RgX_ooyE7sRdJOJ_2FhO0kzi0GCqYktItpI1c_I28w0xMy5Clq9iwO4lgfxKFVT2Yz9do-ax2ob6KdJCOR8VBCVoJAqT-4agYEFyyXgKMrozXeDVQkW38_M8o5CGU16rIPtZ8NKt3H0hl1'
    ids = []
    equipment = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for row in cur.execute('SELECT * FROM telegram_users'):
        ids.append(str(row[1]))
    if str(cid) in ids:
        for row in cur.execute(f'SELECT * FROM telegram_users WHERE message_chat_id = {cid}'):
            if mt == 'Мои данные':
                bot.send_message(cid, f'''Мы не в праве (да и не в силах) собирать о Вас личную информацию. Вот всё, что у нас есть:
ID: {row[1]}
Фамилия: {row[2]}
Имя: {row[3]}
Отчество: {row[4]}
Ник: {row[5]}''', reply_markup=main_buttons)
            elif mt == 'Назад':
                bot.send_message(cid, 'Что бы Вы хотели сделать?', reply_markup=main_buttons)
            elif mt == 'О нас':
                bot.send_photo(cid, logo_original)
                time.sleep(0.1)
                for row in cur.execute('SELECT * FROM about_us_text'):
                    bot.send_message(cid, row[1], reply_markup=main_buttons)
            elif mt == 'Оборудование':
                for row in cur.execute('SELECT * FROM Equipment'):
                    equipment.add(row[1].replace('_', ' '))
                equipment.add('Назад')
                bot.send_message(cid, 'Оборудование UCK:', reply_markup=equipment)
            elif mt == 'Контакты':
                bot.send_message(cid, 'Казахстан, Карагандинская область, г. Караганда, Ул.Ленина, строение 6\nТел: +7 (7212) 922-572, +7 (775) 915-0910')
                for row in cur.execute('SELECT * FROM Contacts'):
                    contacts = f'''{row[1]}
{row[2]}
Телефон: {row[3]}
               {row[4]}
Эл. почта: {row[5]}
               {row[6]}'''.replace('None', '')
                    bot.send_message(cid, contacts, reply_markup=main_buttons)
            elif mt == 'Галерея':
                pass
            elif mt == 'Сотрудники':
                pass
            for row in cur.execute('SELECT * FROM Equipment'):
                if mt == row[1].replace('_', ' '):
                    bot.send_photo(cid, row[5])
                    time.sleep(0.1)
                    answer = row[3]
                    bot.send_message(cid, answer, reply_markup=equipment)

    elif str(cid) not in ids:
        registration(message)

def delete_me(message):
    con = sqlite3.connect('UCK.sqlite3')
    cur = con.cursor()
    cid = message.chat.id
    nick = message.from_user.first_name
    mt = message.text

bot.polling(none_stop = True)