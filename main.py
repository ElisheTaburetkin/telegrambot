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

def main():

    # START KEYBOARD
    watch_ob = InlineKeyboardButton('Смотреть объявления', callback_data='watch')
    create_ob = InlineKeyboardButton('Создать объявление', callback_data='create')
    startkb = InlineKeyboardMarkup(row_width=1).add(watch_ob,create_ob)

    # CATEGORY KEYBOARD
    med = InlineKeyboardButton('Медицина', callback_data='Медицина')
    sport = InlineKeyboardButton('Спорт', callback_data='Спорт')
    cnck = InlineKeyboardButton('Назад', callback_data='cancel')
    #ctkb = InlineKeyboardMarkup(row_width=1).add(med,sport,cnck)
    catbuttons = [InlineKeyboardButton('Все категории', callback_data='Все категории'),InlineKeyboardButton('Промышленное', callback_data='Промышленное'),InlineKeyboardButton('Логистика и склад', callback_data='Логистика и склад'),InlineKeyboardButton('Для магазина', callback_data='Для магазина'),InlineKeyboardButton('Для ресторана', callback_data='Для ресторана'),InlineKeyboardButton('Для салона красоты', callback_data='Для салона красоты'),InlineKeyboardButton('Лабораторное', callback_data='Лабораторное'),InlineKeyboardButton('Медицинское', callback_data='Медицинское'),InlineKeyboardButton('Другое', callback_data='Другое'),InlineKeyboardButton('Назад', callback_data='cancel')]
    ctkb = InlineKeyboardMarkup(row_width=1).add(*catbuttons)
    # CANCEL KEYBOARD
    cnck = InlineKeyboardButton('Назад', callback_data='cancel')
    cnkb = InlineKeyboardMarkup(row_width=1).add(cnck)

# start command logic

    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await bot.send_photo(message.chat.id, photo=InputFile("images/doska-obyavlenii.png"), caption="Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей. Подписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",reply_markup=startkb)

# cancel button logic

    @dp.callback_query_handler(lambda c: c.data == 'cancel',state=NewAd)
    async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state=='NewAd:type':
            await state.reset_state()
            await bot.send_photo(callback_query.from_user.id, photo=InputFile("images/doska-obyavlenii.png"),
                                 caption="Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей. Подписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",
                                 reply_markup=startkb)
        elif current_state=='NewAd:name':
            await state.set_state('NewAd:type')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию товара',
                                   reply_markup=ctkb)
        elif current_state == 'NewAd:description':
            await state.set_state('NewAd:name')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Введите название товара',
                                   reply_markup=cnkb)
        elif current_state == 'NewAd:photo':
            await state.set_state('NewAd:description')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Введите описание товара',
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
            await bot.send_photo(callback_query.from_user.id, photo=InputFile("images/doska-obyavlenii.png"),
                                 caption="Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей. Подписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",
                                 reply_markup=startkb)
        elif current_state == 'WatchAd:page':
            await state.set_state('WatchAd:type')
            await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию товара',
                                   reply_markup=ctkb)




# create or watch select

    @dp.callback_query_handler()
    async def newad(callback_query: types.CallbackQuery):
        if callback_query.data == 'create':
            await NewAd.type.set()
            await bot.send_message(chat_id=callback_query.from_user.id,text='Выберите категорию товара',reply_markup=ctkb)
        elif callback_query.data == 'watch':
            await WatchAd.type.set()
            await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите категорию товара',
                                   reply_markup=ctkb)

# create AD logic

    @dp.callback_query_handler(state=NewAd.type)
    async def ad_type(call: types.CallbackQuery,state: FSMContext):
        async with state.proxy() as data:
            data['type'] = call.data
        await call.message.answer('Введите название товара',reply_markup=cnkb)
        await NewAd.next()

    @dp.message_handler(state=NewAd.name)
    async def ad_name(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            data['name'] = message.text
        await message.answer('Введите описание товара',reply_markup=cnkb)
        await NewAd.next()

    @dp.message_handler(state=NewAd.description)
    async def ad_desc(message: types.Message,state: FSMContext):
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
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await message.answer('Отправьте свой userid в телеграмм в виде @userid',reply_markup=cnkb)
        await NewAd.next()

    @dp.message_handler(state=NewAd.userid)
    async def ad_uid(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            data['userid'] = message.text
        await message.answer('Ваш товар отправлен на модерацию!')
        await bot.send_photo(message.chat.id, photo=InputFile("images/doska-obyavlenii.png"),
                             caption="Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей. Подписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",
                             reply_markup=startkb)
        async with state.proxy() as data:
            await db.add_ad(state)
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
            await call.message.answer('Пока объявлений нет:(',reply_markup=cnkb)
        else:
            for i in ads[0]:
                await bot.send_photo(chat_id=call.from_user.id, photo=InputFile(os.getcwd() + i[4]),
                                 caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUserid: {i[6]}\n')
            await call.message.answer('Для просмотра следующей страницы введите необходимое число (например 2)',
                             reply_markup=cnkb)
            await state.set_state('WatchAd:page')
    @dp.message_handler(state=WatchAd.page)
    async def adwatch_page(message: types.Message,state: FSMContext):
        async with state.proxy() as data:
            ads = data['pages']
        if message.text.isdigit()==False or int(message.text)>len(ads):
            await message.answer('Такой страницы не существует!',reply_markup=cnkb)
        else:
            for i in ads[int(message.text)-1]:
                await bot.send_photo(chat_id=message.chat.id, photo=InputFile(os.getcwd() + i[4]),
                                 caption=f' Название: {i[2]}\nОписание: {i[3]}\nЦена: {i[5]}₽\nUserid: {i[6]}\n')
            await message.answer(f'Cтраница {message.text} из {len(ads)}',reply_markup=cnkb)


# polling
    executor.start_polling(dp, skip_updates=True)

# Programming BASE
if __name__=='__main__':
    db = DataBase()
    main()
