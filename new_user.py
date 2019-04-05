import sqlite3 # Импортируем модуль для работы с базой данных SQLite3

def add_user(from_id, group_number): # функция добавления незарегистрированного пользователя в базу данных с помощью SQL-запросов через его id и номер группы, который он указал
    print("Создание пользователя...")
    connaction = sqlite3.connect("mysite//data//data.sqlite3")
    cursor = connaction.cursor()
    cursor.execute("SELECT COUNT (vk_id) FROM students")
    result = cursor.fetchall()
    count = result[0][0] + 1
    #cursor.execute("INSERT INTO students (vk_id) VALUES (@2)", [from_id])
    group_number = str(group_number[0]) + str(group_number[2])
    cursor.execute("INSERT INTO students (vk_id, gr_id) VALUES ({0}, {1})".format(from_id, group_number))
    #cursor.execute("UPDATE students SET gr_id = {0} WHERE id = {1}".format(group_number, count))
    connaction.commit()
    connaction.close()
    #new_group.new_member(group_number, from_id)
    print("Пользователь создан")


def is_auth(from_id): # Функция проверки на присутствие пользователя в базе данных через его id ВКонтакте. Возвращает True, если пользователь авторизован, False - в обратном случае
    connaction = sqlite3.connect("mysite//data//data.sqlite3")
    cursor = connaction.cursor()
    cursor.execute("SELECT id FROM students WHERE vk_id = @1", [from_id])
    result = cursor.fetchall()
    connaction.close()
    if len(result) == 0:
        print("Пользователь не авторизован")
        return False
    elif result[0][0]:
        print("Пользователь авторизован")
        return True


def check_group_member(from_id): # Проверка на то, какой группе пренадлежит пользователь через его id ВКонтакте
    connaction = sqlite3.connect("mysite//data//data.sqlite3", timeout=10)
    cursor = connaction.cursor()
    cursor.execute("SELECT gr_id FROM students WHERE vk_id = {0}".format(from_id))
    result = cursor.fetchall()
    group = result[0][0]
    return group # Возвращается номер группы

def change_group(from_id, new_group): # Функция смены группы в случае ошибки введенных данных, через id ВКонтакте и номер введенной группы
    if str(check_group_member(from_id)) != str(new_group):
        connaction = sqlite3.connect("mysite//data//data.sqlite3")
        cursor = connaction.cursor()
        cursor.execute("UPDATE students SET gr_id = {0} WHERE vk_id = {1}".format(new_group, from_id))
        connaction.commit()
        connaction.close()
        message = "Вы успешно добавлены в группу " + new_group[0] + "." + new_group[1]
    else:
        message = "Вы уже состоите в группе " + new_group[0] + "." + new_group[1]
    return message # Возвращается сообщение об успешном добавлении, либо присутствии пользователя в данной группе