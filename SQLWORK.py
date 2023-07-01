import sqlite3

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('deal4you.db')  # sql connection
        self.cur = self.conn.cursor()
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS AD (id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    name TEXT, description TEXT,
    photo TEXT, price REAL,
    userid TEXT);""")
        self.conn.commit()
    async def add_ad(self,state):
        async with state.proxy() as data:
            self.cur.execute(f"""INSERT INTO AD(type, name, description, photo, price, userid)
                        VALUES('{data['type']}', '{data['name']}', '{data['description']}', '{data['photo']}','{data['price']}','{data['userid']}');""")
            self.conn.commit()
