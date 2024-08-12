from aiogram import types
from states.send_chanell import Form
from loader import dp,bot
from aiogram.dispatcher import FSMContext
import random
from keyboards.inline.main_menu_super_admin import main_menu_keyboard,xbet_types
import re,os
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

PHOTOS_DIR = "photos"




async def delete_previous_message(chat_id: int, state: FSMContext):
    async with state.proxy() as data:
        if 'last_message_id' in data:
            try:
                await bot.delete_message(chat_id, data['last_message_id'])
            except Exception as e:
                print(f"Failed to delete message {data['last_message_id']}: {e}")





@dp.callback_query_handler(lambda c: c.data in ["melbet", "xbet", "xpari", "funpari", "mostbet"])
async def process_callback(callback_query: types.CallbackQuery,state:FSMContext):
    await delete_previous_message(callback_query.message.chat.id, state)
    data = callback_query.data
    links = {
        "melbet": ("https://refpa5169344.top/L?tag=d_3433309m_18649c_&site=3433309&ad=18649",
                   "https://refpakrtsb.top/L?tag=d_3433309m_18775c_&site=3433309&ad=18775"),
        "onewin": ("", ""),
        "xbet": ("https://refpa7921972.top/L?tag=s_3452875m_355c_&site=3452875&ad=355",
                 "https://refpa7921972.top/L?tag=s_3452875m_1524c_apk&site=3452875&ad=1524"),
        "xpari": ("https://xp-aff.com///L?tag=d_3458612m_64821c_site&site=3458612&ad=64821&r=registration",
                  "https://xp-aff.com///L?tag=d_3458612m_71587c_apk1&site=3458612&ad=71587"),
        "funpari": ("https://fpaff.top/L?tag=d_3530145m_79306c_&site=3530145&ad=79306&r=registration",
                    "https://fpaff.top/L?tag=d_3530145m_85380c_&site=3530145&ad=85380"),
        "mostbet": ("https://mostbetnow.com/YXjF?sub1=Bonusi&sub2=500",
                    "https://mostbetnow.com/nXjF?sub1=Yuklab&sub2=Bonus&sub3=Oling")
    }

    reg_link, apk_link = links[data]

    # Inline keyboards with links
    register_apk_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Register", url=reg_link)
            ],
            [
                InlineKeyboardButton(text="APK", url=apk_link)

            ]
        ]
    )
    
    photo_path = 'id.jpg' 
    sent_message  = await bot.send_photo(
        chat_id=callback_query.from_user.id,
        photo=types.InputFile(photo_path),
        caption="Ro'yxatdan o'tganingizdan so'ng ID raqamingizni yuboring!\n"
                "So'ngra botdan signal olishingiz mumkin!\n<b>ID yozish format ID:1234678</b>\n\nОтправьте свой идентификационный номер после регистрации! \nТогда вы можете получить сигнал от бота!\nID формат записи ID:1234678\n\n\nSend your ID number after registration! \nThen you can get a signal from the bot! \nID write format ID:1234678",
        reply_markup=register_apk_keyboard
    )
    await Form.id_number.set()
        # Store the message ID
    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id


@dp.message_handler(lambda message: re.match(r'^ID:\d+$', message.text), state=Form.id_number)
async def capture_user_id(message: types.Message, state: FSMContext):
    await delete_previous_message(message.chat.id, state)
    user_id = message.text.split(':')[1]

    # Send random photo with main menu and get new signal buttons
    photo_path = os.path.join(PHOTOS_DIR, random.choice(os.listdir(PHOTOS_DIR)))
    sent_message = await bot.send_photo(
        chat_id=message.chat.id,
        photo=types.InputFile(photo_path),
        caption="Sizga yangi signal!\nНовый сигнал тебе!\nA new signal to you!",
        reply_markup=main_menu_keyboard
    )
    await state.finish()
    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id


@dp.callback_query_handler(lambda c: c.data == "main_menu")
async def main_menu_callback(callback_query: types.CallbackQuery,state:FSMContext):
    await delete_previous_message(callback_query.message.chat.id, state)
    sent_message = await bot.send_message(callback_query.from_user.id, "🤖SIGNAL OLISH UCHUN XOXLAGAN ILOVANI YUKLAB OLING🔐\n\n🤖DOWNLOAD THE APP YOU WANT TO GET THE SIGNAL🔐\n\n【ЗАГРУЗИТЕ ЛЮБОЕ ПРИЛОЖЕНИЕ, ЧТОБЫ ПОЛУЧИТЬ БУДИЛЬНИК】", reply_markup=xbet_types)
    await state.finish()
    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id



@dp.callback_query_handler(lambda c: c.data == "get_new_signal")
async def get_new_signal_callback(callback_query: types.CallbackQuery,state:FSMContext):
    await delete_previous_message(callback_query.message.chat.id, state)
    photo_path = os.path.join(PHOTOS_DIR, random.choice(os.listdir(PHOTOS_DIR)))
    sent_message = await bot.send_photo(
        chat_id=callback_query.from_user.id,
        photo=types.InputFile(photo_path),
        caption="Sizga yangi signal!",
        reply_markup=main_menu_keyboard
    )
    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id

@dp.message_handler(lambda message: not re.match(r'^ID:\d+$', message.text), state=Form.id_number)
async def incorrect_format(message: types.Message):
    await message.answer("Iltimos, ID raqamingizni quyidagi formatda yuboring: ID:1234567\n\nPlease send your ID number in the following format:ID: 1234567\n\nПожалуйста, отправьте свой идентификационный номер в следующем формате: ID:1234567")
