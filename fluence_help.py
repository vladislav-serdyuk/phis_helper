from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

import phisics_calculator

fluence_form_router = Router()

help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мои опции', callback_data='phis_help_options')]
])

class FluenceForm(StatesGroup):
    ask_power = State()
    ask_diameter = State()

def is_float(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

@fluence_form_router.callback_query(F.data == 'fluence')
async def ask_power(query: CallbackQuery, state: FSMContext):
    await state.set_state(FluenceForm.ask_power)
    await query.message.answer('Введите мощность (Ватты)')

@fluence_form_router.message(lambda m: is_float(m.text), FluenceForm.ask_power)
async def ask_diameter(message: Message, state: FSMContext):
    await state.update_data(power=float(message.text))
    await state.set_state(FluenceForm.ask_diameter)
    await message.answer('Введите диаметр (Милиметры)')

@fluence_form_router.message(lambda m: is_float(m.text), FluenceForm.ask_diameter)
async def say_result(message: Message, state: FSMContext):
    await state.update_data(diameter=float(message.text))
    await message.answer(str(await phisics_calculator.calc_fluence(**await state.get_data())) + ' Дж/м^2',
                         reply_markup=help_keyboard)
    await state.clear()
