# -*- coding: utf-8 -*-
import telebot, sqlite3
from telebot import *
import time
from datetime import date

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
                bot.send_message(cid, '''Напишите свои ФИО через "_".
Пример: Нурпеисов_Ербол_Мендыбаевич
Будьте внимательны!''')
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
    main_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_buttons.add('Мои данные', 'О нас', 'Оборудование')
    main_buttons.add('Галерея', 'Контакты', 'Сотрудники')
    back_to_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_main.add('Назад')
    logo_original = 'https://psv4.userapi.com/c856224/u232799244/docs/d8/ba8ba5cf0adb/logo_original.png?extra=7-u5wDzEK1RgX_ooyE7sRdJOJ_2FhO0kzi0GCqYktItpI1c_I28w0xMy5Clq9iwO4lgfxKFVT2Yz9do-ax2ob6KdJCOR8VBCVoJAqT-4agYEFyyXgKMrozXeDVQkW38_M8o5CGU16rIPtZ8NKt3H0hl1'
    ids = []
    equipment = types.ReplyKeyboardMarkup(resize_keyboard=True)
    video_gallery = types.ReplyKeyboardMarkup(resize_keyboard=True)
    video_gallery.add('UCK видео о компании')
    video_gallery.add('Тест на засыпание водителя')
    video_gallery.add('Галерея')
    employees = types.ReplyKeyboardMarkup(resize_keyboard=True)
    update_delete = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
                bot.send_message(cid, '''Казахстан, Карагандинская область, г. Караганда, Ул.Ленина, строение 6
Тел: +7 (7212) 922-572, +7 (775) 915-0910''')
                for row in cur.execute('SELECT * FROM Contacts'):
                    contacts = f'''{row[1]}
{row[2]}
Телефон: {row[3]}
               {row[4]}
Эл. почта: {row[5]}
               {row[6]}'''.replace('None', '')
                    bot.send_message(cid, contacts, reply_markup=main_buttons)
            elif mt == 'Галерея':
                photo_video = types.ReplyKeyboardMarkup(resize_keyboard=True)
                photo_video.add('Фото', 'Видео')
                photo_video.add('Назад')
                bot.send_message(cid, 'Что Вы хотите посмотреть?', reply_markup=photo_video)
            elif mt == 'Фото':
                photo_gallery = types.ReplyKeyboardMarkup(resize_keyboard=True)
                photo_gallery.add(
                    'Установка cистемы кругового обзора на 360* с функцией видеорегистратора. KAZMinerals')
                photo_gallery.add(
                    'Установка системы контроля и предупреждения усталости водителя')
                photo_gallery.add(
                    'Рабочая поездка на Соколовско-Сарбайское месторождение. ССГПО. ERG')
                photo_gallery.add(
                    'Галерея')
                bot.send_message(cid, 'Все фото:', reply_markup=photo_gallery)
            elif mt == 'Установка cистемы кругового обзора на 360* с функцией видеорегистратора. KAZMinerals':
                bot.send_message(cid, mt)
                for row in cur.execute(f'SELECT * FROM photo_gallery WHERE Name = "{mt}"'):
                    bot.send_photo(cid, row[3])
            elif mt == 'Установка системы контроля и предупреждения усталости водителя':
                bot.send_message(cid, mt)
                for row in cur.execute(f'SELECT * FROM photo_gallery WHERE Name = "{mt}"'):
                    bot.send_photo(cid, row[3])
            elif mt == 'Рабочая поездка на Соколовско-Сарбайское месторождение. ССГПО. ERG':
                bot.send_message(cid, mt)
                for row in cur.execute(f'SELECT * FROM photo_gallery WHERE Name = "{mt}"'):
                    bot.send_photo(cid, row[3])
            elif mt == 'Видео':
                bot.send_message(cid, 'Все видео:', reply_markup=video_gallery)
            elif mt == 'UCK видео о компании':
                video1 = 'https://youtu.be/VS-Rbzk16B4'
                bot.send_message(cid, video1, reply_markup=video_gallery)
            elif mt == 'Тест на засыпание водителя':
                video2 = 'https://www.youtube.com/watch?v=w6_q8PgW_vg'
                bot.send_message(cid, video2, reply_markup=video_gallery)
            elif mt == 'Сотрудники':
                for row in cur.execute('SELECT * FROM Employees ORDER BY F'):
                    if len(str(row[4])) == 2:
                        str_day = str(row[4])
                    elif len(str(row[4])) == 1:
                        str_day = '0' + str(row[4])
                    else:
                        str_day = '01'
                    if len(str(row[5])) == 2:
                        str_month = str(row[5])
                    elif len(str(row[5])) == 1:
                        str_month = '0' + str(row[5])
                    else:
                        str_month = '01'
                    if len(str(row[6])) == 4:
                        str_year = str(row[6])
                    else:
                        str_year = '2000'
                    if int(row[5]) < int(time.strftime('%m')):
                        age = str(int(time.strftime('%Y')) - int(row[6]))
                    elif int(row[5]) > int(time.strftime('%m')):
                        age = str(int(time.strftime('%Y')) - int(row[6]) - 1)
                    elif int(row[5]) == int(time.strftime('%m')):
                        if int(row[4]) < int(time.strftime('%d')):
                            age = str(int(time.strftime('%Y')) - int(row[6]))
                        elif int(row[4]) >= int(time.strftime('%d')):
                            age = str(int(time.strftime('%Y')) - int(row[6]) - 1)
                    employeer = row[1] + ' ' + row[2] + ' ' + row[3] + ', ' + age + '\n' + row[8] + '\n' + row[7]
                    employees.add(employeer)
                employees.add('Добавить запись')
                employees.add('Назад')
                bot.send_message(cid, 'Сотрудники Umbrella Corporation Kazakhstan', reply_markup=employees)
            elif mt == 'Изменить':
                pre_message = str(message.message_id - 2)
                bot.send_message(cid, pre_message)
            elif mt == 'Добавить запись':
                bot.send_message(cid, '''Чтобы добавить запись, отправьте данные, разделяя их  символом
" | ". Пример:
Фамилия Имя Отчество | 01.01.1991 | Отдел | Должность''')
            elif ' | ' in mt:
                datas = mt.split(' | ')
                billy = 0
                for x in datas:
                    billy += 1
                if billy == 4:
                    fio = datas[0]
                    b_date = datas[1]
                    department = datas[2].capitalize()
                    position = datas[3].capitalize()
                else:
                    bot.send_message(cid, 'Проверьте правильность написания!')
                fio = fio.split(' ')
                count = 0
                for i in fio:
                    count += 1
                if count == 3:
                    name1 = fio[0].capitalize()
                    name2 = fio[1].capitalize()
                    name3 = fio[2].capitalize()
                elif count == 2:
                    name1 = fio[0].capitalize()
                    name2 = fio[1].capitalize()
                    name3 = ''
                else:
                    bot.send_message(cid, 'Проверьте правильность написания ФИО!')
                b_date = b_date.split('.')
                b_count = 0
                for r in b_date:
                    b_count += 1
                if b_count == 3:
                    b_day = b_date[0]
                    b_month = b_date[1]
                    b_year = b_date[2]
                else:
                    bot.send_message(cid, 'Проверьте правильность написания даты!')
                try:
                    b_day = int(b_day)
                    b_month = int(b_month)
                    b_year = int(b_year)
                    date(b_year, b_month, b_day)
                    cur.execute('INSERT INTO Employees (F, I, O, Day, Month, Year, Department, Position) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (name1, name2, name3, int(b_day), int(b_month), int(b_year), department, position))
                    con.commit()
                    bot.send_message(cid, ':)', reply_markup=employees)
                    bot.send_message(888833912, f'Пользователь {cid}/{nick} добавил запись: Сотрудники ({name1}, {name2}, {name3}, {int(b_day)}, {int(b_month)}, {int(b_year)}, {department}, {position})')
                except:
                    bot.send_message(cid, 'Проверьте правильность написания!')
                    bot.send_message(888833912, f'Пользователь {cid}/{nick} пытался добавить запись: Сотрудники ({mt})')
            for row in cur.execute('SELECT * FROM Employees'):
                if row[1] + ' ' + row[2] + ' ' + row[3] in mt:
                    if row[8] + '\n' + row[7] in mt:
                        update_delete.add('Изменить')
                        update_delete.add('Удалить')
                        update_delete.add('Сотрудники')
                        fio = row[1] + ' ' + row[2] + ' ' + row[3]
                        bot.send_message(cid, fio, reply_markup=update_delete)
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
