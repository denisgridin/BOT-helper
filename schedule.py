from keys import * # Импорт ключей, для работы с расписанием
import sqlite3, new_user # Импорт модуля для работы с базами данных, модуля для работы с базами пользователей


def result_for_bottom(group, day, from_id): # Результат для нижней дня нижней недели
    connaction = sqlite3.connect('Bot-helper//data//data.sqlite3')
    #connaction = sqlite3.connect('data//data.sqlite3')
    cursor = connaction.cursor()
    cursor.execute("SELECT {0} FROM {1};".format(day, group))
    result = cursor.fetchall()
    cursor.close()
    return result # Возвращается список результата

def result_for_top(group, day, from_id): # Результат для нижней дня верхней недели
    connaction = sqlite3.connect('Bot-helper//data//data.sqlite3')
    #connaction = sqlite3.connect('data//data.sqlite3')
    cursor = connaction.cursor()
    cursor.execute("SELECT {0} FROM {1} ;".format(day, group))
    result = cursor.fetchall()
    cursor.close()
    return result # Возвращается список результата


def get_message(day, text, from_id): # Функция для составления исходящего сообщения 
    group = "g_" + str(new_user.check_group_member(from_id))
    if text[-1:] in keys_bottom or text[-6:] in keys_bottom:
        day = day + "_bot"
        result, count = result_for_bottom(group, day, from_id)
    elif text[-1:] in keys_top or text[-7:] in keys_top:
        day = day + "_top"
        result, count = result_for_top(group, day, from_id)
    count = int(count[0][0])
    message = "Расписание по запросу:  " + text + '\n'
    time = ['8:00-9:35', '9:50-11:25', '11:55-13:30', '13:45-15:20', '15:50-17:25', '17:40-19:15']
    i = 0
    while i in range(0,6):
        if result[i][0] == None:
            message += '\n' + str(i + 1) + '. ' + '⏰ ' + time[i] + '📌 ' + "Окно"
            i += 1
        else:
            message += '\n' + str(i + 1) + '. ' + '⏰ ' +  time[i] + '📌 '+ str(result[i][0])
            i += 1
    return message # Возвращается сообщение

def get_day(text): # Получение номера дня и возврат через return
    n = 1
    for n in keys_days:
        if text[:2] in keys_days[n]:
            day = str(n)
            return day
        elif text.split(' ')[0] in keys_days[n]:
            day = str(n)
            return day
        elif text[:1] in keys_days[n]:
            day = str(n)
            return day

def answer(text, from_id): # Функция формирования ответа
    day = get_day(text) # Получение дня
    message = get_message(day, text, from_id) # Получение сообщения, в зависимости от дня
    return message # Текст передается в главную функцию

