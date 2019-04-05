import schedule, keys, person, random, new_user, datetime # Импортируем необходимые модули для работы с сообщением

def check_sched(text): # Функция проверки на пренадлежность пунктам расписания
    isKey1 = False
    isKey2 = False
    isKey3 = False
    for i in keys.keys_days:
        isKey1 += text.split(' ')[0] in keys.keys_days[i]          # Ключ - полное слово
        isKey2 += text[0:2] in keys.keys_days[i]                  # Ключ - которкое слово
        isKey3 += text[0:1] in keys.keys_days[i]                  # Ключ - номер дня
    return isKey1 + isKey2 + isKey3 > 0


def get_week(from_id): # Функция получения расписания на всю неделю
    year = str(new_user.check_group_member(from_id))[0]
    photo = 'photo-171055937_4562390'
    attachment = ""
    if year == '1':
        attachment = photo + "64", photo + "65"
    if year == '2':
        attachment = photo + "61", photo + "62"
    if year == '3':
        attachment = photo + "66", photo + "67"
    if year == '4':
        attachment = photo + "68", photo + "69"
    if year == '5':
        attachment = photo + "70", photo + "71"
    return attachment, year

# Словарь для работы с функцией определения расписания на текущий день
dayOfWeek = {
	'1': "понедельник",
	'2': "вторник",
	'3': "среда",
	'4': "четверг",
	'5': "пятница",
	'6': "суббота",
	'7': "воскресенье"
}

def today(): # Функция определения текущего дня с помощью модуля datetime
	if ((((int(datetime.datetime.today().strftime("%j")) // 7) + 1) // 2) == 1):
		week = 'верхняя'
	else:
		week = 'нижняя'
	day = dayOfWeek[str(datetime.datetime.today().isoweekday())]
	return day + " " + week

def create_message(text, from_id): # Функция создания сообщения, в зависимости от присланного запроса с vk, и возврат через return текста обратного сообщения и прикрепленного вложения
    if check_sched(text):
        message = schedule.answer(text, from_id)
        attachment = ''
        return message, attachment
    elif text == 'начать':
        message = 'Привет, хочешь опробовать бота и узнать расписание? \nТогда действуй по инструкции:\n'
        attachment  = 'photo-171055937_456239063'
        return message, attachment
    elif 'сегодня' in text:
        text = today()
        message = schedule.answer(text, from_id)
        attachment = ''
        return message, attachment
    elif 'сменить' in text:
        group = text.split(" ")[1][0] + text.split(" ")[1][2]
        if new_user.is_auth(from_id):
            message = new_user.change_group(from_id, group)
            attachment = ""
        else:
            message = "Вы пока что не состоите ни в одной группе.\nПожалуйста, введи номер группы, как показано в примере. Например: Группа 1.1"
            attachment = ""
        return message, attachment

    elif 'неделя' in text:
        attachment, year = get_week(from_id)
        message = 'Расписание на неделю для '+ year +  ' курса\n'
        return message, attachment
    elif text.split(' ')[0] == 'инфо':
        if len(text[1]) > 0:
            text = text.split(' ')[1] + ' ' + text.split(' ')[2]
            message, attachment = person.check_person(text)
        else:
            message = "Ошибка! Пожалуйста, введите данные преподавателя в формате 'Фамилия И.О'"
            attachment = ''
        return message, attachment
    elif(text[0:11] == 'как думаешь'):
        answers = ["да","нет","возможно","вероятно, да","вероятно, нет","мб","нет","точно не знаю","наверное","уверенно","определенно да","определенно нет","по-любому","конечно","оставь меня","поживем-увидим","не хочу отвечать","не хочу тебя растраивать"]
        num = int(random.randint(0,17))
        message = str(answers[num])
        attachment = ''
        return message, attachment
    elif(text[0:5] == 'салам'):
        message = "Ваалейкум ассалам"
        attachment = ''
        return message, attachment
    elif(text[0:6] == 'привет'):
        message = "Привет"
        attachment = ''
        return message, attachment
    elif (text[0:7] == "спасибо"):
        message = "Не за что, обращайся"
        attachment = ''
        return message, attachment
    else:
        err = ['Я тебя не понимаю. Напиши "Помощь", чтобы узнать мои команды', 'Даже не знаю, что сказать. Напиши "Помощь", чтобы узнать мои команды', 'Мне нечего сказать на этот счет. Напиши "Помощь", чтобы узнать мои команды', 'Подумай над своими словами. Напиши "Помощь", чтобы узнать мои команды', 'Я бы на твоем месте выбрал что-нибудь другое. Напиши "Помощь", чтобы узнать мои команды', 'Похоже, я ничего не могу сказать. Напиши "Помощь", чтобы узнать мои команды', 'Может пойдем по плану? Напиши "Помощь", чтобы узнать мои команды', 'У меня нет данных по этому поводу. Напиши "Помощь", чтобы узнать мои команды', 'Не знаю такого. Напиши "Помощь", чтобы узнать мои команды', 'Почему ты спрашиваешь у меня такое? Мои команды ты можешь узнать, написав "Помощь"', 'Боже мой, можно по-понятнее? Напиши "Помощь", чтобы узнать мои команды']
        num = int(random.randint(0, len(err) - 1))
        message = str(err[num])
        attachment = ""
        return message, attachment