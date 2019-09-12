from flask import Flask, request, json # Импортируется фреймворк flask, а также с ним в пакете request, для работы с запросами и json, для раскодирования запроса с vkapi
import requests
import sqlite3, vk, json, random # импортируется vk, для работы с api, sqlite3 для работы с базами данных
from keys import * # импортируется созданный модуль keys, в котором находятся необходимые ключи, для работы с расписанием
from settings import * # импортируется модуль settings, в котором прописываются токены, для доступа к группе вк с ботом
import make_kboard, Message, new_user # Импортируются рукописные модули: make_kboard - создание клавиатуры в зависимости от запроса, Message - модуль обработки и оправки сообщений, new_user - модуль работы с базой данных студентов

app = Flask(__name__) # Подключение к фреймворку Flask
@app.route('/', methods=['POST']) # задается параметр POST для отправки сообщений
def processing(): # Главная функция 
    #Распаковываем json из пришедшего POST-запроса
    global data
    data = json.loads(request.data)
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation': #Проверка сервера на подтверждение
        return confirmation_token
    elif data['type'] == 'message_new': #Если пришло сообщение, то обрабатываем его
        #Задаем начальные значения и настройки сессии
        session = vk.Session()
        global api
        api = vk.API(session, v=5.92)
        from_id = data['object']['from_id']
        global text
        is_conversation = data['object']['id'] == 0
        text = data['object']['text'].lower()
        random_id = random.randint(10000,99999)
        not_found = False
        attachment = ''
        menu = ['календарь', 'помощь', 'меню'] # Кортеж для разделов меню
        need_auth = ['сегодня', 'неделя'] # Кортеж элементов, при которых нужна регистрация в базе данных
        # Обработка запроса, если сообщение пришло из беседы
        if "бот," in text:
            text = text[5:]
            global peer_id, chat_id
            peer_id = data['object']['peer_id']
            chat_id = int(peer_id-2000000000)
            from_id = data['object']['from_id']
            if (text[0:3] == 'кто'):
                count_users = api.messages.getConversationMembers(peer_id=peer_id,access_token=token)['count']
                num = int(random.randint(0,count_users-1))
                message = str(api.messages.getConversationMembers(peer_id=peer_id,access_token=token)['profiles'][num]['first_name'] + ' ' + api.messages.getConversationMembers(peer_id=peer_id,access_token=token)['profiles'][num]['last_name'])
                attachment = ''
            else:
                message, attachment  = Message.create_message(text, from_id)
                print(message)
            api.messages.send(access_token=token, chat_id=str(chat_id), random_id=random_id, message=message, attachment = attachment)
        # Обработка запроса, если сообщение пришло из личных сообщений    
        elif is_conversation == False :
            from_id = data['object']['from_id']
            group_number = '3.6'
            if text in menu:
                message = 'Отрываю ' + text + '...'
                attachment = ''
                if 'календарь' in text:
                    if new_user.is_auth(from_id) == False:
                        message = "Пожалуйста, введи номер группы, как показано в примере. Например: Группа 1.1"
                        print("Пожалуйста, введи номер группы, как показано в примере. Например: Группа 1.1")
                        api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment)
                    else:
                        kboard = make_kboard.create_kboard(text)
                        api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard )
                        print("Получение расписания")
                elif text == 'помощь':
                    message = 'Почитай обо мне в этой статье!'
                    attachment = 'wall-171055937_21'
                    kboard = make_kboard.create_kboard('меню')
                    api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard)
                else:
                    kboard = make_kboard.create_kboard(text)
                    api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard )

            elif 'группа' in text:
                if new_user.is_auth(from_id) == False:
                    group_number = text[-3::]
                    new_user.add_user(from_id, group_number)
                    message = "Спасибо, вы успешно внесены в базу"
                    kboard = make_kboard.create_kboard('меню')
                    print(message)
                    api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard )
                else:
                    message = "Вы уже в базе"
                    kboard = make_kboard.create_kboard('меню')
                    print(message)
                    api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard )
            elif Message.check_sched(text) == True:
                print("Есть контакт")
                if new_user.is_auth(from_id) == True:
                    try:
                        message, attachment  = Message.create_message(text, from_id)
                        kboard = make_kboard.create_kboard('календарь')
                        print(message)
                        api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard)
                    except:
                        message = "Нет данных для вашей группы"
                        attachment = ""
                        kboard = make_kboard.create_kboard('меню')
                        print(message)
                        api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard)
                else:
                    message = "Пожалуйста, введи номер группы, как показано в примере. Например: Группа 1.1"
                    attachment = ''
                    print("Пожалуйста, введи номер группы, как показано в примере. Например: Группа 1.1")
                    print(message)
                    api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment)
            else:
                print("Другой запрос")
                kboard = make_kboard.create_kboard('меню')
                message, attachment = Message.create_message(text, from_id)
                api.messages.send(access_token=token, from_id=str(from_id), random_id=random_id, message=message, attachment = attachment, keyboard = kboard )
    return 'ok' # Возвращаемое значение всегда должно быть 'ok' - иначе возникнет ошибка

    #api.messages.send() - метод отправки сообщений
    #api.messages.getConversationMembers() - метод получения участников беседы, в которой произошел запрос