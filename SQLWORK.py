import sqlite3
import os
from datetime import date,timedelta,datetime
import matplotlib.pyplot as plt

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
                if counter%3!=0:
                    ad.append(i)
                    if counter==len(ads):
                        ADS.append(ad)
                    counter += 1
                elif counter%3==0:
                    ad.append(i)
                    ADS.append(ad)
                    ad=[]
                    counter += 1
                    page += 1
        else:
            ads = self.cur.execute(f""" SELECT * FROM AD_MAIN;""").fetchall()
            counter = 1
            page = 1
            ADS=[]
            ad=[]
            for i in ads:
                if counter%3!=0:
                    ad.append(i)
                    if counter==len(ads):
                        ADS.append(ad)
                    counter += 1
                elif counter%3==0:
                    ad.append(i)
                    ADS.append(ad)
                    ad=[]
                    counter += 1
                    page += 1
        return ADS

    async def moder_ad(self):
        return self.cur.execute(f""" SELECT * FROM AD;""").fetchall()

    async def watch_delete_ad(self):
        ads = self.cur.execute(f""" SELECT * FROM AD_MAIN;""").fetchall()
        counter = 1
        page = 1
        ADS = []
        ad = []
        for i in ads:
            if counter % 3 != 0:
                ad.append(i)
                if counter == len(ads):
                    ADS.append(ad)
                counter += 1
            elif counter % 3 == 0:
                ad.append(i)
                ADS.append(ad)
                ad = []
                counter += 1
                page += 1
        return ADS

    async def delete_ad(self, id):
        try:
            ad = self.cur.execute(f""" SELECT * FROM AD_MAIN WHERE id='{id}';""").fetchone()
            photo = ad[4]
            if len(self.cur.execute(f""" SELECT * FROM AD WHERE photo='{photo}';""").fetchall()) == 0 and len(
                    self.cur.execute(f""" SELECT * FROM AD_MAIN WHERE photo='{photo}';""").fetchall()) == 1:
                os.remove(os.getcwd() + photo)
            self.cur.execute(f"""DELETE FROM AD_MAIN WHERE id='{id}';""")
            self.conn.commit()
        except:
            pass

    async def reject_ad(self, id):
        try:
            ad = self.cur.execute(f""" SELECT * FROM AD WHERE id='{id}';""").fetchone()
            photo = ad[4]
            if len(self.cur.execute(f""" SELECT * FROM AD WHERE photo='{photo}';""").fetchall())==1 and len(self.cur.execute(f""" SELECT * FROM AD_MAIN WHERE photo='{photo}';""").fetchall())==0:
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

    async def get_stats(self):
        users = self.cur.execute(f""" SELECT * FROM USERS;""").fetchall()
        quantity_users = len(users)
        mount_ago = date.today() - timedelta(days=31)
        users_last_mounth = []
        for i in users:
            dat = i[1].split('-')
            dat = date(int(dat[0]), int(dat[1]), int(dat[2]))
            if dat >= mount_ago:
                users_last_mounth.append(i)
        users_last_mounth = len(users_last_mounth)
        on_moder_ads = len(self.cur.execute(f""" SELECT * FROM AD;""").fetchall())
        ads = len(self.cur.execute(f""" SELECT * FROM AD_MAIN;""").fetchall())

        labels = ['Промышленное','Логистика и склад','Для магазина','Для ресторана','Для салона красоты','Лабораторное','Медицинское','Другое']
        values = []
        labelsn = []
        for i in labels:
            clv = len(self.cur.execute(f""" SELECT * FROM AD_MAIN WHERE type='{i}';""").fetchall())
            if clv==0:
                pass
            else:
                values.append(clv)
                labelsn.append(i)
        labels = labelsn
        fig1, ax1 = plt.subplots()
        wedges, texts, autotexts = ax1.pie(values, labels=labels, autopct='%1.2f%%')
        ax1.axis('equal')
        filename = str(datetime.utcnow()).replace(' ','_').replace('.',':',1).replace(':','-')
        plt.savefig(os.getcwd()+f'\\images\\stats\\{filename}.png')
        return [f'Пользователи: {quantity_users} ({users_last_mounth} за последние 31 день)\nОбъявлений: {ads}\nОбъявлений на модерации: {on_moder_ads}',filename]





