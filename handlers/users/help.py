from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from loader import dp

#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.message_handler(CommandHelp(),state='*')
async def bot_help(message: types.Message,state:FSMContext):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Firdavs",url="https://t.me/FIRDAVS_SELEF")]])
    await message.answer("ADMIN BILAN BOG'LANISH",reply_markup=kb)
    await state.finish()