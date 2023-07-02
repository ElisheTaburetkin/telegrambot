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
    async def get_ad(self, type):
        ads = self.cur.execute(f""" SELECT * FROM AD WHERE type='{type}';""").fetchall()
        counter = 1
        page = 1
        ADS=[]
        ad=[]
        for i in ads:
            if counter!=3:
                ad.append(i)
                if counter==len(ads):
                    ADS.append(ad)
                counter += 1
            elif counter%3==0:
                ad.append(i)
                ADS.append(ad)
                ad=[]
                page += 1
        return ADS