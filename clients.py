import sqlite3


db = sqlite3.connect('clients.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS clients (
        name TEXT,
        TelegramId TEXT,
        path TEXT
        )""")


db.commit()


def fill_clients_from_file():
    file = open("users.txt", 'r', encoding='utf-8')

    mas = file.readlines()
    mas2 = []
    for i in mas:
        sql.execute(f"INSERT INTO clients VALUES (?,?,?)", (f"{i[:-1]}", '0', '0'))

    db.commit()

def add_client(name, id):
    sql.execute(f"INSERT INTO clients VALUES (?,?,?)", (f"{name}", f'{id}', '0'))
    db.commit()

def get_client_list():
    for values in sql.execute("SELECT * FROM clients WHERE TelegramId != '0'"):
        print(values)


def get_all_client_list():
    for values in sql.execute("SELECT * FROM clients"):
        print(values)

def delete_all():
    inp = input("Вы собираетесь удалить всю базу. Вы уверены?(Y/N): ")
    if inp == "Y":
        sql.execute("DELETE FROM clients")
        db.commit()
        print("База удалена")
    else:
        print("Ошибка")

#fill_clients_from_file()

get_all_client_list()