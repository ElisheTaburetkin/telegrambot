from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton,InputFile
from aiogram.dispatcher.filters import Text
from bot_config import *
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
def main():
    #START KEYBOARD=======================================================================
    watch_ob = InlineKeyboardButton('Смотреть объявления', callback_data='button1')
    create_ob = InlineKeyboardButton('Создать объявление', callback_data='button2')
    startkb = InlineKeyboardMarkup(row_width=2).add(watch_ob,create_ob)

    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await bot.send_photo(message.chat.id, photo=InputFile("images/doska-obyavlenii.png"), caption="Широкий выбор промышленного оборудования от надежных производителей. На нашей доске объявлений вы найдете станки, резаки, пресс-формы и многое другое для различных отраслей. Подписывайтесь на наш канал, чтобы быть в курсе новостей и специальных предложений.",reply_markup=startkb)


    executor.start_polling(dp, skip_updates=True)


if __name__=='__main__':
    main()