import os

from aiogram import Router, F, Bot
from aiogram.methods import GetFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ContentType, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup

import phisics_calculator

spector_form_router = Router()

help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои опции', callback_data='phis_help_options')]
])

class SpectorForm(StatesGroup):
    ask_file = State()

@spector_form_router.callback_query(F.data == 'spector')
async def ask_from(query: CallbackQuery, state: FSMContext):
    await state.set_state(SpectorForm.ask_file)
    await query.message.answer('Отправте файл со спектром')

@spector_form_router.message(F.content_type == ContentType.DOCUMENT)
async def say_result(message: Message, state: FSMContext, bot: Bot):
    spector_file_id = message.document.file_id
    spector_file_info = await bot(GetFile(file_id=spector_file_id))
    spector_file = await bot.download_file(spector_file_info.file_path)
    spector_data = spector_file.read()
    output_image_file_path, resonance, wight = await phisics_calculator.calc_spector(spector_data.decode('utf-8-sig'))
    await message.answer_photo(FSInputFile(output_image_file_path))
    await message.answer(f'Положение резонанса: {resonance} нм\n'
                         f'Ширена на полувысоте: {wight} нм', reply_markup=help_keyboard)
    os.remove(output_image_file_path)
    await state.clear()
