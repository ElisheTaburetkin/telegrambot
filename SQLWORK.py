import sqlite3
import os
from datetime import date

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('deal4you.db')  # sql connection
        self.cur = self.conn.cursor()
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS AD (id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    name TEXT, description TEXT,
    photo TEXT, price REAL,
    userid TEXT, userfromid TEXT);""")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS AD_MAIN (id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        name TEXT, description TEXT,
        photo TEXT, price REAL,
        userid TEXT, date TEXT);""")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS USERS (id INTEGER, date TEXT);""")
        self.conn.commit()

    async def add_user(self, id):
        if self.cur.execute(f"""SELECT * FROM USERS WHERE id='{id}'""").fetchone() == None:
            self.cur.execute(f"""INSERT INTO USERS(id, date) VALUES('{id}','{date.today()}')""")
            self.conn.commit()

    async def add_ad(self, state, userfromid):
        async with state.proxy() as data:
            self.cur.execute(f"""INSERT INTO AD(type, name, description, photo, price, userid, userfromid)
                        VALUES('{data['type']}', '{data['name']}', '{data['description']}', '{data['photo']}','{data['price']}','{data['userid']}','{userfromid}');""")
            self.conn.commit()

    async def get_ad(self, type):
        if type!='Все категории':
            ads = self.cur.execute(f""" SELECT * FROM AD_MAIN WHERE type='{type}';""").fetchall()
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
        else:
            ads = self.cur.execute(f""" SELECT * FROM AD_MAIN;""").fetchall()
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

    async def moder_ad(self):
        return self.cur.execute(f""" SELECT * FROM AD;""").fetchall()

    async def reject_ad(self, id):
        try:
            ad = self.cur.execute(f""" SELECT * FROM AD WHERE id='{id}';""").fetchone()
            photo = ad[4]
            os.remove(os.getcwd() + photo)
            self.cur.execute(f"""DELETE FROM AD WHERE id='{id}';""")
            self.conn.commit()
            return [int(ad[7]), f'Ваше объявление {ad[2]}, {ad[5]}₽ не прошло модерацию!❌']
        except:
            pass

    async def accept_ad(self, id):
        try:
            ad = self.cur.execute(f""" SELECT * FROM AD WHERE id='{id}';""").fetchone()
            self.cur.execute(f"""DELETE FROM AD WHERE id='{id}';""")
            self.cur.execute(f"""INSERT INTO AD_MAIN(type, name, description, photo, price, userid, date)
                        VALUES('{ad[1]}', '{ad[2]}', '{ad[3]}', '{ad[4]}','{ad[5]}','{ad[6]}','{date.today()}');""")
            self.conn.commit()
            return [int(ad[7]),f'Ваше объявление {ad[2]}, {ad[5]}₽ прошло модерацию и опубликовано!✅']
        except:
            pass
