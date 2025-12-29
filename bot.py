import os
import asyncio

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from translate_help import translate_form_router
from spector_help import spector_form_router
from fluence_help import fluence_form_router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()
router = Router()
router.include_routers(translate_form_router, spector_form_router, fluence_form_router)

action_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перевод величин',
                          callback_data='translate')],
    [InlineKeyboardButton(text='Вычисление резонанса',
                          callback_data='spector')],
    [InlineKeyboardButton(text='Вычисление флюенса',
                          callback_data='fluence')]
])


@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Привет, я твой помошник, я могу:\n"
                         f"1. Переводить частоту излучения или энергию фотона в длину волны света и обратно.\n"
                         f"2. Вычислять по спектру в формате .txt положение резонанса и его ширины на полувысоте.\n"
                         f"3. Вычислять флюенс лазерной системы по средней мощности.", reply_markup=action_keyboard)

@router.callback_query(F.data == 'phis_help_options')
async def phis_help_options(query: CallbackQuery):
    await query.message.answer(f"Мои опцииㅤㅤ", reply_markup=action_keyboard)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
