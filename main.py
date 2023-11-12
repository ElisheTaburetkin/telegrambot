#!/usr/bin/python
# -*- coding: utf-8 -*-
# aiogram
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton,InputFile
from aiogram.dispatcher.filters import Text

# bot config
from bot_config import *

#for watch project dir
import os

# Database
from SQLWORK import DataBase
import sqlite3

# creating bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)

# States
class NewAd(StatesGroup):
    type = State()
    name = State()
    description = State()
    photo = State()
    price = State()
    userid = State()

class WatchAd(StatesGroup):
    type = State()
    pages = State()
    page = State()

class Admin(StatesGroup):
    AdminPannel = State()
    DeleteAds = State()

class Myads(StatesGroup):
    pages = State()
    page = State()




def main():

    # START KEYBOARD
    watch_ob = InlineKeyboardButton('Смотреть объявления', callback_data='watch')
    create_ob = InlineKeyboardButton('Создать объявление', callback_data='create')
    my_ads = InlineKeyboardButton('Мои объявления', callback_data='my_ads')
    admin_rev = InlineKeyboardButton('Связь с администратором', url='t.me/myth75')
    rules = InlineKeyboardButton('Правила пользования', callback_data='rules')
    video_guide = InlineKeyboardButton('Видеоинструкция', callback_data='video')
    startkb = InlineKeyboardMarkup(row_width=1).add(watch_ob,create_ob,my_ads,admin_rev,rules,video_guide)

    # ADMIN KEYBOARD
    admin_buttons = ['Модерация объявлений✔', 'Удаление объявлений🗑️', 'Статистика📊', 'Выход🏃']
    admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    admin_kb.add(*admin_buttons)

    # CATEGORY KEYBOARD
    catbuttons = [
                  InlineKeyboardButton('Недвижимость Москва и МО', callback_data='Недвижимость Москва и МО'),
                  InlineKeyboardButton('Недвижимость Санкт-Петербург и ЛО', callback_data='Недвижимость Санкт-Петербург и ЛО'),
                  InlineKeyboardButton('Недвижимость Краснодарский край', callback_data='Недвижимость Краснодарский край'),
                  InlineKeyboardButton('Недвижимость другие регионы РФ', callback_data='Недвижимость другие регионы РФ'),
                  InlineKeyboardButton('Зарубежная недвижимость', callback_data='Зарубежная недвижимость'),
                  InlineKeyboardButton('Коммерческая недвижимость', callback_data='Коммерческая недвижимость'),
                  InlineKeyboardButton('Аренда Москва', callback_data='Аренда Москва'),
                  InlineKeyboardButton('Аренда регионы РФ', callback_data='Аренда регионы РФ'),
                  InlineKeyboardButton('Продажа бизнеса', callback_data='Продажа бизнеса'),
                  InlineKeyboardButton('Продажа оборудования', callback_data='Продажа оборудования'),
                  InlineKeyboardButton('Другое', callback_data='Другое'),
                  InlineKeyboardButton('Назад', callback_data='cancel')]
    ctkb = InlineKeyboardMarkup(row_width=1).add(*catbuttons)

    catcrbuttons = [
                  InlineKeyboardButton('Недвижимость Москва и МО', callback_data='Недвижимость Москва и МО'),
                  InlineKeyboardButton('Недвижимость Санкт-Петербург и ЛО', callback_data='Недвижимость Санкт-Петербург и ЛО'),
                  InlineKeyboardButton('Недвижимость Краснодарский край', callback_data='Недвижимость Краснодарский край'),
                  InlineKeyboardButton('Недвижимость другие регионы РФ', callback_data='Недвижимость другие регионы РФ'),
                  InlineKeyboardButton('Зарубежная недвижимость', callback_data='Зарубежная недвижимость'),
                  InlineKeyboardButton('Коммерческая недвижимость', callback_data='Коммерческая недвижимость'),
                  InlineKeyboardButton('Аренда Москва', callback_data='Аренда Москва'),
                  InlineKeyboardButton('Аренда регионы РФ', callback_data='Аренда регионы РФ'),
                  InlineKeyboardButton('Продажа бизнеса', callback_data='Продажа бизнеса'),
                  InlineKeyboardButton('Продажа оборудования', callback_data='Продажа оборудования'),
                  InlineKeyboardButton('Другое', callback_data='Другое'),
                  InlineKeyboardButton('Назад', callback_data='cancel')]
    ctkbc = InlineKeyboardMarkup(row_width=1).add(*catcrbuttons)

    # CANCEL KEYBOARD
    cnck = InlineKeyboardButton('Назад', callback_data='cancel')
    cnkb = InlineKeyboardMarkup(row_width=1).add(cnck)

    # GM KEYBOARD
    cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
    gmkb = InlineKeyboardMarkup(row_width=1).add(cnck)

    # start func
    async def start_message_send(userid):
        await db.add_user(userid)
        await bot.send_photo(userid, photo=InputFile("images/doska-obyavlenii.png"),
                             caption=f"Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей.\nПользователей бота: {await db.get_len_users()} , размещено объявлений: {await db.get_len_ads()}.\nПодписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",
                             reply_markup=startkb)

# start command logic

    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        #await db.add_user(message.from_user.id)
        #await bot.send_photo(message.chat.id, photo=InputFile("images/doska-obyavlenii.png"), caption=f"Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей.\nПользователей бота: {await db.get_len_users()} , размещено объявлений: {await db.get_len_ads()}.\nПодписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",reply_markup=startkb)
        await start_message_send(message.from_user.id)
# admin command logic
    @dp.message_handler(commands=['admin'])
    async def process_admin_command(message: types.Message,state: FSMContext):
        await message.answer('Проверка доступа...')
        if str(message.from_user.id) in ADMINUID:
            await message.answer('Доступ к панели администратора получен!✅',reply_markup=admin_kb)
            await state.set_state('Admin:AdminPannel')
        else:
            await message.answer('Отказано в доступе❌')

# cancel button logic

    @dp.callback_query_handler(lambda c: c.data == 'cancel',state=NewAd)
    async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state=='NewAd:type':
            await state.reset_state()
            await start_message_send(callback_query.from_user.id)
        elif current_state=='NewAd:name':
            await state.set_state('NewAd:type')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию товара',
                                   reply_markup=ctkbc)
        elif current_state == 'NewAd:description':
            await state.set_state('NewAd:name')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Введите название товара(до 66 символов)',
                                   reply_markup=cnkb)
        elif current_state == 'NewAd:photo':
            await state.set_state('NewAd:description')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Введите описание товара(до 650 символов)',
                                   reply_markup=cnkb)
        elif current_state == 'NewAd:price':
            await state.set_state('NewAd:photo')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Отправьте фото товара',
                                   reply_markup=cnkb)
        elif current_state == 'NewAd:userid':
            await state.set_state('NewAd:price')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Введите цену товара',
                                   reply_markup=cnkb)

    @dp.callback_query_handler(lambda c: c.data == 'cancel', state=WatchAd)
    async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state == 'WatchAd:type':
            await state.reset_state()
            await start_message_send(callback_query.from_user.id)
        elif current_state == 'WatchAd:page':
            await state.set_state('WatchAd:type')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию товара',
                                   reply_markup=ctkb)

    @dp.callback_query_handler(lambda c: c.data == 'cancel', state=Myads)
    async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
        await state.reset_state()
        await start_message_send(callback_query.from_user.id)


# create or watch select

    @dp.callback_query_handler()
    async def newad(callback_query: types.CallbackQuery, state: FSMContext):
        if callback_query.data == 'create':
            await NewAd.type.set()
            await bot.send_message(chat_id=callback_query.from_user.id,text='Выберите категорию товара',reply_markup=ctkbc)

        elif callback_query.data == 'watch':
            await WatchAd.type.set()
            await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию товара',
                                   reply_markup=ctkb)

        elif callback_query.data == 'video':
            await bot.send_video(callback_query.from_user.id, open('images/videoguide.mp4', 'rb'))

        elif callback_query.data == 'rules':
            text = u"""
            Запрещено размещение:
•	Объявлений о продаже запрещенных товаров и услуг.
•	Объявлений о несуществующих и неактуальных предложениях.
•	Объявлений, не дающих исчерпывающего представления о товаре или услуге.
•	Объявлений с заведомо ложной информацией о товаре или услуге (цена в ценнике и в описании должна совпадать, название и описание объявлений должны соответствовать товару, изображенному на фотографиях, и т.п.)
Объявлений с информацией, которая:
1.	содержит угрозы, дискредитирует, оскорбляет, порочит честь и достоинство или деловую репутацию, или нарушает неприкосновенность частной жизни других пользователей или третьих лиц;
2.	нарушает права несовершеннолетних лиц;
3.	является вульгарной или непристойной, содержит порнографические изображения и тексты или сцены сексуального характера с участием несовершеннолетних; содержит нецензурную брань, бранные слова и выражения, не относящиеся к нецензурной брани;
4.	содержит информацию о жестоком обращении с животными;
5.	содержит описание средств и способов суицида, любое подстрекательство к его совершению;
6.	пропагандирует и/или способствует разжиганию расовой, религиозной, этнической ненависти или вражды, пропагандирует фашизм или идеологию расового превосходства;
7.	содержит экстремистские материалы;
8.	пропагандирует преступную деятельность или содержит советы, инструкции или руководства по совершению преступных действий
9.	содержит информацию ограниченного доступа, включая, но не ограничиваясь, государственной и коммерческой тайной, информацией о частной жизни третьих лиц;
10.	содержит рекламу или описывает привлекательность употребления наркотических веществ, в том числе «цифровых наркотиков» (звуковых файлов, оказывающих воздействие на мозг человека за счет бинауральных ритмов), информацию о распространении наркотиков, рецепты их изготовления и советы по употреблению;
11.	носит мошеннический характер;
12.	нарушает интеллектуальные права третьих лиц;
13.	содержит спам, в том числе в виде простого набора букв в объявлении, в том числе в названии и/или описании товара, размещения объявлений в отношении несуществующих товаров
14.	нарушает иные права и интересы граждан и юридических лиц или требования законодательства Российской Федерации;
15.	описывает способы заработка в интернете, содержит информацию о казино, тотализаторах, любых азартных играх и пари;
16.	содержит описание финансовых пирамид;
17.	является политической рекламой.
            """
            await bot.send_message(chat_id=callback_query.from_user.id,text=text)

        elif callback_query.data == 'my_ads':
            await Myads.pages.set()
            async with state.proxy() as data:
                data['pages'] = await db.get_my_ads(callback_query.from_user.id)
                data['page'] = 1
                ads = data['pages']
            if len(ads) == 0:
                await callback_query.message.answer('Пока объявлений нет:(', reply_markup=gmkb)
            else:
                for i in ads[0]:
                    buttons = [InlineKeyboardButton('Удалить🗑️', callback_data=f'delete_{i[0]}')]
                    kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
                    await bot.send_photo(chat_id=callback_query.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n', reply_markup=kb)


                if len(ads) > 1:
                    next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                    cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                    pagekb = InlineKeyboardMarkup(row_width=2).add(cnck, next)
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
                elif len(ads) == 1:
                    cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                    pagekb = InlineKeyboardMarkup(row_width=2).add(cnck)
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)

# Watch my ads logic
    @dp.message_handler(state=Myads.pages)
    async def adwatch_page_my(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            ads = data['pages']
        if message.text.isdigit() == False or int(message.text) > len(ads):
            cnck = InlineKeyboardButton('Назад', callback_data='cancel')
            kb = InlineKeyboardMarkup(row_width=1).add(cnck)
            await message.answer('Такой страницы не существует!', reply_markup=kb)
        else:
            async with state.proxy() as data:
                data['page'] = int(message.text)
            for i in ads[int(message.text) - 1]:
                buttons = [InlineKeyboardButton('Удалить🗑️', callback_data=f'delete_{i[0]}')]
                kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
                await bot.send_photo(chat_id=message.chat.id, photo=InputFile(os.getcwd() + i[4]),
                                     caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n',reply_markup=kb)
            await message.answer(f'Cтраница {message.text} из {len(ads)}')
            if message.text == '1':
                if len(ads) > 1:
                    cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                    next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                    pagekb = InlineKeyboardMarkup(row_width=2).add(cnck, next)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
            elif message.text == str(len(ads)) and message.text != '1':
                cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                pagekb = InlineKeyboardMarkup(row_width=2).add(cnck, last)
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                       reply_markup=pagekb)
            else:
                next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                pagekb = InlineKeyboardMarkup(row_width=2).add(last, next, cnck)
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                       reply_markup=pagekb)

    @dp.callback_query_handler(state=Myads.pages)
    async def pagebutns_my(callback_query: types.CallbackQuery,state=FSMContext):
        if callback_query.data == 'nextpage':
            try:
                async with state.proxy() as data:
                    ads = data['pages']
                    page = int(data['page'])
                if page > len(ads):
                    await callback_query.message.answer('Такой страницы не существует!', reply_markup=gmkb)
                else:
                    async with state.proxy() as data:
                        data['page'] += 1
                        page = data['page']
                    for i in ads[page - 1]:
                        buttons = [InlineKeyboardButton('Удалить🗑️', callback_data=f'delete_{i[0]}')]
                        kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n',reply_markup=kb)
                    await callback_query.message.answer(f'Cтраница {page} из {len(ads)}')
                    if str(page) == '1':
                        if len(ads) > 1:
                            cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                            next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                            pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,next)
                            await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                               reply_markup=pagekb)
                    elif str(page) == str(len(ads)) and str(page) != '1':
                        cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,last)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
                    else:
                        next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(last, next, cnck)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
            except Exception as inst:
                print(inst)
                await bot.send_message(chat_id=callback_query.from_user.id, text='Bot exception!')

        elif callback_query.data == 'lastpage':
            try:
                async with state.proxy() as data:
                    ads = data['pages']
                    page = int(data['page'])
                if page > len(ads):
                    await callback_query.message.answer('Такой страницы не существует!', reply_markup=gmkb)
                else:
                    async with state.proxy() as data:
                        data['page'] -= 1
                        page = data['page']
                    for i in ads[page - 1]:
                        buttons = [InlineKeyboardButton('Удалить🗑️', callback_data=f'delete_{i[0]}')]
                        kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n',reply_markup=kb)
                    await callback_query.message.answer(f'Cтраница {page} из {len(ads)}')
                    if str(page) == '1':
                        if len(ads) > 1:
                            cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                            next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                            pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,next)
                            await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                               reply_markup=pagekb)
                    elif str(page) == str(len(ads)) and str(page) != '1':
                        cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,last)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
                    else:
                        next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        cnck = InlineKeyboardButton('Назад', callback_data='cancel')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(last, next, cnck)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
            except:
                await bot.send_message(chat_id=callback_query.from_user.id, text='Bot exception!')

        elif callback_query.data[:6] == 'delete':
            id_ad = int(callback_query.data[7:])
            await db.delete_ad(id_ad)
            async with state.proxy() as data:
                data['pages'] = await db.get_my_ads(callback_query.from_user.id)
            await callback_query.message.delete()

# Admin logic

    @dp.message_handler(state=Admin.AdminPannel)
    async def admin(message: types.Message,state: FSMContext):
        if message.text=='Выход🏃':
            await state.reset_state()
            await message.answer('Вы вышли из панели администратора!❌',reply_markup=types.ReplyKeyboardRemove())
            await start_message_send(message.from_user.id)
        elif message.text=='Модерация объявлений✔':
            ads = await db.moder_ad()
            if len(ads)==0:
                await message.answer('Нет объявлений для модерации')
            else:
                for i in ads:
                    buttons = [InlineKeyboardButton('Отклонить❌', callback_data=f'reject_{i[0]}'),InlineKeyboardButton('Принять✅', callback_data=f'accept_{i[0]}')]
                    kb = InlineKeyboardMarkup(row_width=2).add(*buttons)
                    await bot.send_photo(chat_id=message.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                     caption=f'Категория: {i[1]}\nНазвание: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n',reply_markup=kb)
        elif message.text=='Удаление объявлений🗑️':
            await state.set_state('Admin:DeleteAds')
            ads = await db.watch_delete_ad()
            async with state.proxy() as data:
                data['DeletAds'] = ads
            if len(ads) == 0:
                await message.answer('Пока объявлений нет:(', reply_markup=cnkb)
            else:
                for i in ads[0]:
                    buttons = [InlineKeyboardButton('Удалить🗑️', callback_data=f'delete_{i[0]}')]
                    kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
                    await bot.send_photo(chat_id=message.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n',reply_markup=kb)
                await message.answer('Для просмотра следующей страницы введите необходимое число (например 2)',
                                          reply_markup=cnkb)
        elif message.text == 'Статистика📊':
            result = await db.get_stats()
            await message.answer(result[0])
            await bot.send_photo(chat_id=message.from_user.id,photo=InputFile(os.getcwd()+'/images/stats/' + result[1] + '.png'), caption='Статистика объявлений по категориям')

    @dp.message_handler(state=Admin.DeleteAds)
    async def adwatch_page(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            ads = data['DeletAds']
        if message.text.isdigit() == False or int(message.text)>len(ads):
            await message.answer('Такой страницы не существует!',reply_markup=cnkb)
        else:
            for i in ads[int(message.text)-1]:
                buttons = [InlineKeyboardButton('Удалить🗑️', callback_data=f'delete_{i[0]}')]
                kb = InlineKeyboardMarkup(row_width=1).add(*buttons)
                await bot.send_photo(chat_id=message.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                     caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n',
                                     reply_markup=kb)
            await message.answer(f'Cтраница {message.text} из {len(ads)}',reply_markup=cnkb)

    @dp.callback_query_handler(state=Admin.AdminPannel)
    async def api(call: types.CallbackQuery, state: FSMContext):
        if call.data[:6]=='reject':
            id_ad = int(call.data[7:])
            result = await db.reject_ad(id_ad)
            await call.message.delete()
            try:
                await bot.send_message(result[0], result[1])
            except:
                pass
        if call.data[:6]=='accept':
            id_ad = int(call.data[7:])
            result = await db.accept_ad(id_ad)
            await call.message.delete()
            try:
                if TGCHANNEL:
                    i = result[2]
                    await bot.send_photo(chat_id=TGCHANNEL, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f'#новоеобъявление\nКатегория: {i[1]}\nНазвание: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n')
                await bot.send_message(result[0],result[1])
            except:
                pass

    @dp.callback_query_handler(state=Admin.DeleteAds)
    async def api_del(call: types.CallbackQuery, state: FSMContext):
        if call.data=='cancel':
            await state.set_state('Admin:AdminPannel')
            await call.message.answer('Вы вышли на главную страницу админ панели')
        elif call.data[:6]=='delete':
            id_ad = int(call.data[7:])
            await db.delete_ad(id_ad)
            async with state.proxy() as data:
                data['DeletAds'] = await db.watch_delete_ad()
            await call.message.delete()


# create AD logic

    @dp.callback_query_handler(state=NewAd.type)
    async def ad_type(call: types.CallbackQuery,state: FSMContext):
        async with state.proxy() as data:
            data['type'] = call.data
        await call.message.answer('Введите название товара(до 66 символов)',reply_markup=cnkb)
        await NewAd.next()

    @dp.message_handler(state=NewAd.name)
    async def ad_name(message: types.Message,state: FSMContext):
        if len(message.text)>66:
            await message.answer('Длина названия больше 66!!')
        else:
            async with state.proxy() as data:
                data['name'] = message.text
            await message.answer('Введите описание товара(до 650 символов)',reply_markup=cnkb)
            await NewAd.next()

    @dp.message_handler(state=NewAd.description)
    async def ad_desc(message: types.Message,state: FSMContext):
        if len(message.text)>650:
            await message.answer('Длина описания больше 650!!')
        else:
            async with state.proxy() as data:
                data['description'] = message.text
            await message.answer('Отправьте фото товара',reply_markup=cnkb)
            await NewAd.next()

    @dp.message_handler(lambda message: not message.photo,state=NewAd.photo)
    async def ad_photo_check(message: types.Message):
        await message.answer('Это не фото!')

    @dp.message_handler(content_types=['photo'],state=NewAd.photo)
    async def ad_photo(message: types.Message,state: FSMContext):
        await message.photo[-1].download(destination_dir=f'{os.getcwd()}/images')
        photo_id = message.photo[-1].file_id
        file_info = await bot.get_file(photo_id)
        async with state.proxy() as data:
            data['photo'] = f'/images/{file_info.file_path}'
        await message.answer('Введите цену товара',reply_markup=cnkb)
        await NewAd.next()

    @dp.message_handler(state=NewAd.price)
    async def ad_price(message: types.Message,state: FSMContext):
        try:
            async with state.proxy() as data:
                data['price'] = float(message.text)
            await message.answer(f'Отправьте свой username в телеграмм в виде @userid или номер телефона, если в ответ вы отправите ".", то ваш юзернейм(@{message.from_user.username}) будет указан автоматически.', reply_markup=cnkb)
            await NewAd.next()
        except:
            await message.answer('Цена должна быть числом!')

    @dp.message_handler(state=NewAd.userid)
    async def ad_uid(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            if message.text == '.':
                data['userid'] = f'@{message.from_user.username}'
            else:
                data['userid'] = message.text
            userfromid = message.from_user.id
        await message.answer('Ваше объявление отправлено на модерацию!')
        await start_message_send(message.from_user.id)
        async with state.proxy() as data:
            await db.add_ad(state, userfromid)
        await state.finish()

# watch AD logic

    @dp.callback_query_handler(state=WatchAd.type)
    async def adwatch_type(call: types.CallbackQuery, state: FSMContext):
        async with state.proxy() as data:
            data['pages'] = await db.get_ad(call.data)
            data['page'] = 1
        async with state.proxy() as data:
            ads = data['pages']

        if len(ads)==0:
            await state.set_state('WatchAd:page')
            await call.message.answer('Пока объявлений нет:(',reply_markup=gmkb)
        else:
            for i in ads[0]:
                await bot.send_photo(chat_id=call.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                 caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n')
            #await call.message.answer('ㅤ',
                             #reply_markup=cnkb)
            await state.set_state('WatchAd:page')
            if len(ads)>1:
                next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,next)
                await bot.send_message(chat_id=call.from_user.id,text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',reply_markup=pagekb)
            elif len(ads)==1:
                cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                pagekb = InlineKeyboardMarkup(row_width=2).add(cnck)
                await bot.send_message(chat_id=call.from_user.id,text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',reply_markup=pagekb)


    @dp.message_handler(state=WatchAd.page)
    async def adwatch_page(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            ads = data['pages']
        if message.text.isdigit() == False or int(message.text)>len(ads):
            await message.answer('Такой страницы не существует!',reply_markup=gmkb)
        else:
            async with state.proxy() as data:
                data['page'] = int(message.text)
            for i in ads[int(message.text)-1]:
                await bot.send_photo(chat_id=message.chat.id, photo=InputFile(os.getcwd() + i[4]),
                                 caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n')
            await message.answer(f'Cтраница {message.text} из {len(ads)}')
            if message.text == '1':
                if len(ads) > 1:
                    cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                    next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                    pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,next)
                    await bot.send_message(chat_id=message.from_user.id,text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',reply_markup=pagekb)
            elif message.text == str(len(ads)) and message.text!='1':
                cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,last)
                await bot.send_message(chat_id=message.from_user.id,text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',reply_markup=pagekb)
            else:
                next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                pagekb = InlineKeyboardMarkup(row_width=2).add(last,next,cnck)
                await bot.send_message(chat_id=message.from_user.id,text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',reply_markup=pagekb)

    @dp.callback_query_handler(state=WatchAd.page)
    async def pagebutns(callback_query: types.CallbackQuery,state=FSMContext):
        if callback_query.data == 'nextpage':
            try:
                async with state.proxy() as data:
                    ads = data['pages']
                    page = int(data['page'])
                if page > len(ads):
                    await callback_query.message.answer('Такой страницы не существует!', reply_markup=gmkb)
                else:
                    async with state.proxy() as data:
                        data['page'] += 1
                        page = data['page']
                    for i in ads[page - 1]:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n')
                    await callback_query.message.answer(f'Cтраница {page} из {len(ads)}')
                    if str(page) == '1':
                        if len(ads) > 1:
                            cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                            next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                            pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,next)
                            await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                               reply_markup=pagekb)
                    elif str(page) == str(len(ads)) and str(page) != '1':
                        cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,last)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
                    else:
                        next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(last, next, cnck)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
            except Exception as inst:
                print(inst)
                await bot.send_message(chat_id=callback_query.from_user.id, text='Bot exception!')

        elif callback_query.data == 'lastpage':
            try:
                async with state.proxy() as data:
                    ads = data['pages']
                    page = int(data['page'])
                if page > len(ads):
                    await callback_query.message.answer('Такой страницы не существует!', reply_markup=gmkb)
                else:
                    async with state.proxy() as data:
                        data['page'] -= 1
                        page = data['page']
                    for i in ads[page - 1]:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                         caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUsername/телефон: {i[6]}\n')
                    await callback_query.message.answer(f'Cтраница {page} из {len(ads)}')
                    if str(page) == '1':
                        if len(ads) > 1:
                            cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                            next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                            pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,next)
                            await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                               reply_markup=pagekb)
                    elif str(page) == str(len(ads)) and str(page) != '1':
                        cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(cnck,last)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
                    else:
                        next = InlineKeyboardButton('Следующая страница', callback_data='nextpage')
                        last = InlineKeyboardButton('Предыдущая страница', callback_data='lastpage')
                        cnck = InlineKeyboardButton('Главное меню', callback_data='cancel')
                        pagekb = InlineKeyboardMarkup(row_width=2).add(last, next, cnck)
                        await bot.send_message(chat_id=callback_query.from_user.id, text='Кнопки навигации по страницам. Вы также можете ввести номер необходимой страницы.',
                                           reply_markup=pagekb)
            except:
                await bot.send_message(chat_id=callback_query.from_user.id, text='Bot exception!')

# polling
    executor.start_polling(dp, skip_updates=True)

# Programming BASE
if __name__=='__main__':
    db = DataBase()
    main()
