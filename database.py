import os
import sqlite3
import random

db = sqlite3.connect('clients.db')
sql = db.cursor()

def get_list_dir_from_db(id) -> list:
    sql.execute(f"SELECT * FROM clients WHERE TelegramId = {id}")
    return os.listdir(sql.fetchone()[2])


def set_dir_in_db(id, dir):
    sql.execute(f"UPDATE clients SET path = '{dir}' WHERE TelegramId = {id}")
    db.commit()


def start_buttons_dict(list_dir) -> dict:
    dict_start_path = {}
    start_buttons_mas = [i[i.rfind("\\")+1:] for i in read_file_in_mas(list_dir)]
    for i in range(len(read_file_in_mas(list_dir))):
        dict_start_path[start_buttons_mas[i]] = read_file_in_mas(list_dir)[i]
    return dict_start_path

def get_dir_from_db(id):
    sql.execute(f"SELECT * FROM clients WHERE TelegramId = {id}")
    return sql.fetchone()[2]

def get_back_dir(id):
    sql.execute(f"SELECT * FROM clients WHERE TelegramId = {id}")
    dir = sql.fetchone()[2]
    return dir[:dir.rfind("\\")]

def registration(message_text: str, message_id: int) -> str:
    db = sqlite3.connect('clients.db')
    sql = db.cursor()
    try:
        sql.execute(f"SELECT * FROM clients WHERE name = '{message_text}'")
        if sql.fetchone() != None:
            sql.execute(f"SELECT * FROM clients WHERE name = '{message_text}'")
            if sql.fetchone()[1] == '0':
                if check_id_base(message_id) == False or check_id_base(message_id) == None:
                    return "1"
                else:
                    return "Ошибка клиента. ID существует. Обратитесь в канал поддержки"
            else:
                return "Ошибка клиента. ID существует. Обратитесь в канал поддержки"
        else:
            return "Ошибка регистрации"

    except:
        return "Ошибка"


def check_id_base(message_id: int) -> bool:
    try:
        sql.execute(f"SELECT * FROM clients WHERE TelegramId = '{message_id}'")
        if sql.fetchone() != None:
            return True
        else:
            return False
    except:
        return False

def read_file_in_mas(file):
    with open(file, encoding='utf-8-sig') as file:
        mas = [i.split("\n") for i in file.readlines()]
        res = []
        for i in range(len(mas)):
            res.append(mas[i][0])
        return res


def get_name(id):
    sql.execute(f"SELECT name FROM clients WHERE TelegramId = '{id}'")
    res = sql.fetchone()[0]

    try:
        return res.split(" ")[1]
    except:
        return res

def admin_get():
    lists = ''
    for values in sql.execute("SELECT * FROM clients"):
        lists += values[0] + " " + values[1] + "\n"
    return lists

def generate_key():
    return random.randint(10000, 999999)

def get_mail_from_db(name):
    sql.execute(f"SELECT * FROM clients WHERE name = '{name}'")
    return sql.fetchone()[3]

def set_key_in_db(name):
    sql.execute(f"UPDATE clients SET code = '{generate_key()}' WHERE name = '{name}'")
    db.commit()

def get_key_from_db(name):
    sql.execute(f"SELECT * FROM clients WHERE name = '{name}'")
    return sql.fetchone()[4]

def set_id_in_db(name, tgid):
    sql.execute(f"UPDATE clients SET TelegramId = '{tgid}' WHERE name = '{name}'")
    db.commit()
#print(read_file_in_mas(dirs_txt))
# print(start_buttons_dict(dirs_txt))
#print(registration("Аликин Александр", 807761312))
#print(check_id_base(807761312))
#test_reg()
#аprint(admin_get())
#set_key_in_db('Александр')


