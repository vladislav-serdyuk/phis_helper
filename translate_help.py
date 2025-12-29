from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

import phisics_calculator

translate_form_router = Router()

help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои опции', callback_data='phis_help_options')]
])

class TranslateForm(StatesGroup):
    ask_from = State()
    ask_to = State()
    ask_input_data = State()

def is_float(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

@translate_form_router.callback_query(F.data == 'translate')
async def ask_from(query: CallbackQuery, state: FSMContext):
    await state.set_state(TranslateForm.ask_from)
    from_select = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Частота излучения',
                              callback_data='translate_from_f')],
        [InlineKeyboardButton(text='Энергия фотона',
                              callback_data='translate_from_e')],
        [InlineKeyboardButton(text='Длина волны',
                              callback_data='translate_from_l')]
    ])
    await query.message.answer('Укажите из чего перевести', reply_markup=from_select)

@translate_form_router.callback_query(F.data.startswith('translate_from'), TranslateForm.ask_from)
async def ask_to(query: CallbackQuery, state: FSMContext):
    await state.update_data({'from': query.data.rsplit('_', maxsplit=1)[-1]})
    await state.set_state(TranslateForm.ask_to)
    from_select = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Частота излучения',
                              callback_data='translate_to_f')],
        [InlineKeyboardButton(text='Энергия фотона',
                              callback_data='translate_to_e')],
        [InlineKeyboardButton(text='Длина волны',
                              callback_data='translate_to_l')]
    ])
    await query.message.answer('Укажите во что перевести', reply_markup=from_select)

@translate_form_router.callback_query(F.data.startswith('translate_to'), TranslateForm.ask_to)
async def ask_input_data(query: CallbackQuery, state: FSMContext):
    await state.update_data({'to': query.data.rsplit('_', maxsplit=1)[-1]})
    await state.set_state(TranslateForm.ask_input_data)
    messages = {'e': 'Введите энергию фотона (Джоули)',
                'l': 'Введите длину волны фотона (Нанометры)',
                'f': 'Введите частоту фотона (Терагерцы)'}
    await query.message.answer(messages[(await state.get_data())['from']])

@translate_form_router.message(lambda m: is_float(m.text), TranslateForm.ask_input_data)
async def say_result(message: Message, state: FSMContext):
    await state.update_data({'data': float(message.text)})
    await message.answer(str(await phisics_calculator.calc_translate((await state.get_data())['from'],
                                                                     (await state.get_data())['to'],
                                                                     (await state.get_data())['data']))
                         + {'e': ' Дж', 'l': ' нм', 'f': ' ТГц'}[(await state.get_data())['to']],
                         reply_markup=help_keyboard)
    await state.clear()
