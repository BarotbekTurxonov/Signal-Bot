from time import sleep
#Dasturchi @Mrgayratov kanla @Kingsofpy
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
import logging
from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from filters import IsUser, IsSuperAdmin, IsGuest
from filters.admins import IsAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, main_menu_for_admin,get_signal,xbet_types
from loader import dp, db, bot
from states.send_chanell import SuperAdminStateChannel
logging.basicConfig(level=logging.INFO)


async def delete_previous_message(chat_id: int, state: FSMContext):
    async with state.proxy() as data:
        if 'last_message_id' in data:
            try:
                await bot.delete_message(chat_id, data['last_message_id'])
            except Exception as e:
                print(f"Failed to delete message {data['last_message_id']}: {e}")


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def get_video(msg: types.Message):
    await msg.reply(msg.video.file_id)

@dp.callback_query_handler(text="start",state='*')
async def bot_echo(message: CallbackQuery,state:FSMContext):
    await delete_previous_message(message.message.chat.id, state)
    await bot.send_video(message.from_user.id,"BAACAgIAAxkBAAJATma6cENS7rGiIAmMX3sf4LdL6wHpAAI4XgACoYHQSW-RZc5_m9sNNQQ",caption="Botdan foydalanish haqida qo'llanma!")
    user = message.from_user
    try:
        db.add_user(user_id=user.id,name=user.first_name)
    except:
        pass

    sent_message = await bot.send_message(chat_id=user.id,text="🤖SIGNAL OLISH UCHUN XOXLAGAN ILOVANI YUKLAB OLING🔐\n\n🤖DOWNLOAD THE APP YOU WANT TO GET THE SIGNAL🔐\n\n【ЗАГРУЗИТЕ ЛЮБОЕ ПРИЛОЖЕНИЕ, ЧТОБЫ ПОЛУЧИТЬ БУДИЛЬНИК】",reply_markup=xbet_types)

    await state.finish()

    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id


@dp.message_handler(IsAdmin(), CommandStart(), state='*')
async def bot_start_admin(message: types.Message):
    await message.answer(f"Assalom alaykum Admin, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_admin)

@dp.message_handler(IsSuperAdmin(), CommandStart(), state="*")
async def bot_start_super_admin(message: types.Message):
    await message.answer(f"Assalom alaykum Bosh Admin, {message.from_user.full_name}!",
                         reply_markup=main_menu_for_super_admin)

@dp.message_handler(IsGuest(), CommandStart(), state="*")
async def bot_start(message: types.Message,state:FSMContext):
    await delete_previous_message(message.chat.id, state)

    user = message.from_user
    try:
        db.add_user(user_id=user.id,name=user.first_name)
    except:
        pass
    if 2 == len(message.text.split(' ')) > 0:
        return await idsave(message, message.text.split(' ')[1])
    user_id = message.from_user.first_name
    sent_message = await message.reply(f"🤖SIGNAL OLISH UCHUN XOXLAGAN ILOVANI YUKLAB OLING🔐\n\n🤖DOWNLOAD THE APP YOU WANT TO GET THE SIGNAL🔐\n\n【ЗАГРУЗИТЕ ЛЮБОЕ ПРИЛОЖЕНИЕ, ЧТОБЫ ПОЛУЧИТЬ БУДИЛЬНИК】",reply_markup=xbet_types)
    await state.finish()
    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id


@dp.message_handler(IsUser(), CommandStart(), state="*")
async def bot_start(message: types.Message,state:FSMContext):
    await delete_previous_message(message.chat.id, state)

    user = message.from_user
    try:
        db.add_user(user_id=user.id,name=user.first_name)
    except:
        pass
    if 2 == len(message.text.split(' ')) > 0:
        return await idsave(message, message.text.split(' ')[1])
    user_id = message.from_user.first_name
    sent_message = await message.reply(f"🤖SIGNAL OLISH UCHUN XOXLAGAN ILOVANI YUKLAB OLING🔐\n\n🤖DOWNLOAD THE APP YOU WANT TO GET THE SIGNAL🔐\n\n【ЗАГРУЗИТЕ ЛЮБОЕ ПРИЛОЖЕНИЕ, ЧТОБЫ ПОЛУЧИТЬ БУДИЛЬНИК】",reply_markup=xbet_types)
    await state.finish()
    async with state.proxy() as data:
        data['last_message_id'] = sent_message.message_id




import requests
from aiogram.types import Message
from loader import dp





@dp.message_handler(IsSuperAdmin(),content_types=['document'])
async def echo(message: types.Message,state:FSMContext):
    try:
        file_id = message.document.file_id
        caption = message.caption
        if caption == None: caption = ''
        user_id = message.from_user.id
        db.add_files(type="document", file_id=file_id, caption=caption, user_id=user_id)
        id_send = db.select_files(user_id=user_id)
        sql_id = ''
        for idsend in id_send:
            sql_id = idsend[0]
        link = await bot.get_me()
        bot_user = f"https://t.me/{link.username}?start={sql_id}"
        await state.update_data({"bot_user": bot_user,"sql_id":sql_id,})
        await message.answer(f"Yaxsh endi kanalga yuborish uchun post kiritin... Content turi hohishi.\n\ncode {sql_id}")
        await SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELD.set()
    except:
        await message.answer("Xatolik yuzaga keldi, qayta urinb ko'ring 😔")

@dp.message_handler(IsSuperAdmin(), state=SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELD,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    msg = await message.answer(f"🕒 Kuting...\n")
    malumot = await state.get_data()

    code_link = malumot.get("bot_user")
    code_str = malumot.get("sql_id")
    await bot.copy_message(chat_id="-1001655834191", from_chat_id=message.chat.id,
                           message_id=message.message_id, caption=f"{message.caption}\n\ncode : <code>{code_str}</code>",
                           reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 Yuklab olish",url=f"{code_link}")), parse_mode=types.ParseMode.HTML)

    sleep(0.5)
    await msg.delete()
    await message.answer("✅ Post muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    await state.finish()

@dp.message_handler(IsSuperAdmin(),content_types=['video'])
async def echo(message: types.Message,state:FSMContext):
    try:
        file_id = message.video.file_id
        caption = message.caption
        if caption == None: caption = ''
        user_id = message.from_user.id
        db.add_files(type="video", file_id=file_id, caption=caption, user_id=user_id)
        id_send = db.select_files(user_id=user_id)
        sql_id = ''
        for idsend in id_send:
            sql_id = idsend[0]
        link = await bot.get_me()
        bot_user = f"https://t.me/{link.username}?start={sql_id}"
        await state.update_data({"bot_user": bot_user,"sql_id":sql_id,})
        await message.answer(f"Yaxsh endi kanalga yuborish uchun post kiritin... Content turi hohishi.\n\ncode {sql_id}")
        await SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELV.set()
    except:
        await message.answer("Xatolik yuzaga keldi, qayta urinb ko'ring 😔")

@dp.message_handler(IsSuperAdmin(), state=SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELV,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    msg = await message.answer(f"🕒 Kuting...\n")
    malumot = await state.get_data()

    code_link = malumot.get("bot_user")
    code_str = malumot.get("sql_id")
    await bot.copy_message(chat_id="-1001655834191", from_chat_id=message.chat.id,
                           message_id=message.message_id, caption=f"{message.caption}\n\ncode : <code>{code_str}</code>",
                           reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 Yuklab olish",url=f"{code_link}")), parse_mode=types.ParseMode.HTML)
    sleep(0.5)
    await msg.delete()
    await message.answer("✅ Post muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    await state.finish()

@dp.message_handler(IsSuperAdmin(),content_types=['photo'])
async def echo(message: types.Message,state: FSMContext):
    try:
        file_id = message.photo[0].file_id
        caption = message.caption
        if caption == None: caption = ''
        user_id = message.from_user.id
        db.add_files(type="photo", file_id=file_id, caption=caption, user_id=user_id)
        id_send = db.select_files(user_id=user_id)
        sql_id = ''
        for idsend in id_send:
            sql_id = idsend[0]
        link = await bot.get_me()
        bot_user = f"https://t.me/{link.username}?start={sql_id}"
        await state.update_data({"bot_user": bot_user,"sql_id":sql_id,})
        await message.answer(f"Yaxsh endi kanalga yuborish uchun post kiritin... Content turi hohishi.\n\ncode {sql_id}")
        await SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNEL.set()
    except:
        await message.answer("Xatolik yuzaga keldi, qayta urinb ko'ring 😔")

@dp.message_handler(IsSuperAdmin(), state=SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNEL,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    msg = await message.answer(f"🕒 Kuting...\n")
    malumot = await state.get_data()

    code_link = malumot.get("bot_user")
    code_str = malumot.get("sql_id")
    await bot.copy_message(chat_id="-1001655834191", from_chat_id=message.chat.id,
                           message_id=message.message_id, caption=f"{message.caption}\n\ncode : <code>{code_str}</code>",
                           reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 Yuklab olish",url=f"{code_link}")), parse_mode=types.ParseMode.HTML)
    sleep(0.5)
    await msg.delete()
    await message.answer("✅ Post muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    await state.finish()

@dp.message_handler(IsSuperAdmin(),content_types=['audio'])
async def echo(message: types.Message,state:FSMContext):
    try:
        file_id = message.audio.file_id
        caption = message.caption
        if caption == None: caption = ''
        user_id = message.from_user.id
        db.add_files(type="audio", file_id=file_id, caption=caption, user_id=user_id)
        id_send = db.select_files(user_id=user_id)
        sql_id = ''
        for idsend in id_send:
            sql_id = idsend[0]
        link = await bot.get_me()
        bot_user = f"https://t.me/{link.username}?start={sql_id}"
        await state.update_data({"bot_user": bot_user,"sql_id":sql_id,})
        await message.answer(f"Yaxsh endi kanalga yuborish uchun post kiritin... Content turi hohishi.\n\ncode {sql_id}")
        await SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELA.set()
    except:
        await message.answer("Xatolik yuzaga keldi, qayta urinb ko'ring 😔")

@dp.message_handler(IsSuperAdmin(), state=SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELA,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    msg = await message.answer(f"🕒 Kuting...\n")
    malumot = await state.get_data()

    code_link = malumot.get("bot_user")
    code_str = malumot.get("sql_id")
    await bot.copy_message(chat_id="-1001655834191", from_chat_id=message.chat.id,
                           message_id=message.message_id, caption=f"{message.caption}\n\ncode : <code>{code_str}</code>",
                           reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 Yuklab olish",url=f"{code_link}")), parse_mode=types.ParseMode.HTML)
    sleep(0.5)
    await msg.delete()
    await message.answer("✅ Post muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    await state.finish()

@dp.message_handler(IsSuperAdmin(),content_types=['voice'])
async def echo(message: types.Message,state:FSMContext):
    try:
        file_id = message.voice.file_id
        caption = message.caption
        if caption == None: caption = ''
        user_id = message.from_user.id
        db.add_files(type="voice", file_id=file_id, caption=caption, user_id=user_id)
        id_send = db.select_files(user_id=user_id)
        sql_id = ''
        for idsend in id_send:
            sql_id = idsend[0]
        link = await bot.get_me()
        bot_user = f"https://t.me/{link.username}?start={sql_id}"
        await state.update_data({"bot_user": bot_user,"sql_id":sql_id,})
        await message.answer(f"Yaxsh endi kanalga yuborish uchun post kiritin... Content turi hohishi.\n\ncode {sql_id}")
        await SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELU.set()
    except:
        await message.answer("Xatolik yuzaga keldi, qayta urinb ko'ring 😔")

@dp.message_handler(IsSuperAdmin(), state=SuperAdminStateChannel.SUPER_ADMIN_STATE_CHANNELU,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    msg = await message.answer(f"🕒 Kuting...\n")
    malumot = await state.get_data()

    code_link = malumot.get("bot_user")
    code_str = malumot.get("sql_id")
    await bot.copy_message(chat_id="-1001655834191", from_chat_id=message.chat.id,
                           message_id=message.message_id, caption=f"{message.caption}\n\ncode : <code>{code_str}</code>",
                           reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("📥 Yuklab olish",url=f"{code_link}")), parse_mode=types.ParseMode.HTML)
    sleep(0.5)
    await msg.delete()
    await message.answer("✅ Post muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
    await state.finish()




@dp.message_handler()
async def idsave(message: types.Message, text=None):
    try:
        argument = message.get_args()

        if text == None: text = message.text or argument
        if text.isdigit():
            IDTXT1 = db.select_files(id=text)
            if len(IDTXT1) > 0:
                IDTXT = IDTXT1[0]
                if IDTXT[1] == 'document':
                    await message.answer_document(IDTXT[2], caption=IDTXT[3])
                elif IDTXT[1] == 'video':
                    await message.answer_video(IDTXT[2], caption=IDTXT[3])
                elif IDTXT[1] == 'photo':
                    await message.answer_photo(IDTXT[2], caption=IDTXT[3])
                elif IDTXT[1] == 'audio':
                    await message.answer_audio(IDTXT[2], caption=IDTXT[3])
                elif IDTXT[1] == 'voice':
                    await message.answer_voice(IDTXT[2], caption=IDTXT[3])
            else:
                await message.answer("Hech narsa topilmadi 😔")
    except:
        await message.answer("Xatolik yuzaga keldi, qayta urinb ko'ring 😔")



        