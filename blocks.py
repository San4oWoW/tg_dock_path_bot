import sqlite3


db = sqlite3.connect('block.db')
sql = db.cursor()
#sql.execute("DELETE FROM block")
sql.execute("""CREATE TABLE IF NOT EXISTS block (
        TelegramId INT,
        count INT
        )""")

db.commit()




def check_users():
    db = sqlite3.connect('block.db')
    sql = db.cursor()
    for i in sql.execute(f"SELECT * FROM block"):
        print(i)


def get_count(id):
    db = sqlite3.connect('block.db')
    sql = db.cursor()
    sql.execute(f"SELECT * FROM block WHERE TelegramId = {id}")
    return sql.fetchone()[1]


def set_count(id):
    db = sqlite3.connect('block.db')
    sql = db.cursor()
    sql.execute(f"UPDATE block SET count = {get_count(id) + 1} WHERE TelegramId = {id}")
    db.commit()

def add_user_to_block_base(id):
    db = sqlite3.connect('block.db')
    sql = db.cursor()
    sql.execute(f"SELECT * FROM block WHERE TelegramId = {id}")
    if sql.fetchone() == None:
        sql.execute(f"INSERT INTO block VALUES (?,?)", (id, 0))
        db.commit()


def check_user_in_block_base(id):
    db = sqlite3.connect('block.db')
    sql = db.cursor()
    sql.execute(f"SELECT * FROM block WHERE TelegramId = {id}")
    try:
        if sql.fetchone()[1] > 4:
            return True
        else:
            return False
    except:
        return None

def clear_users_from_base():
    db = sqlite3.connect('block.db')
    sql = db.cursor()
    sql.execute("DELETE FROM block")
    db.commit()



