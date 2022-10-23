import sqlite3


db = sqlite3.connect('clients.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS clients (
        name TEXT,
        TelegramId TEXT,
        path TEXT,
        email TEXT,
        code TEXT
        )""")

db.commit()


def fill_clients_from_file():
    file = open("users.txt", 'r', encoding='utf-8')

    mas = file.readlines()
    mas_new = []
    mas_end = []
    for i in mas:
        mas_new.append(i[0:-1])
    # for i in mas:
    #     sql.execute(f"INSERT INTO clients VALUES (?,?,?,?,?)", (f"{i[:-1]}", '0', '0', '0', '0'))
    for i in mas_new:
        mas_end.append(i.split(" "))

    for i in mas_end:
        sql.execute(f"INSERT INTO clients VALUES (?,?,?,?,?)", (f"{i[0]} {i[1]}", f'{i[3]}', '0', f'{i[2]}', '0'))
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



#delete_all()
#fill_clients_from_file()
get_all_client_list()
#get_all_client_list()