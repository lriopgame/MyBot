from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types

class ReportScenario(StatesGroup):
    waiting_for_type = State()
    waiting_for_params = State()
    waiting_for_confirm = State()

@dp.message_handler(commands='scenario_start')
async def start_scenario(message: types.Message):
    await message.answer('Какой тип отчёта вам нужен? (финансовый / аналитический)')
    await ReportScenario.waiting_for_type.set()

@dp.message_handler(state=ReportScenario.waiting_for_type)
async def process_type(message: types.Message, state: FSMContext):
    report_type = message.text.lower()
    await state.update_data(type=report_type)
    await message.answer('Укажите параметры отчёта (период, источник и т.п.):')
    await ReportScenario.waiting_for_params.set()

@dp.message_handler(state=ReportScenario.waiting_for_params)
async def process_params(message: types.Message, state: FSMContext):
    params = message.text
    await state.update_data(params=params)
    data = await state.get_data()
    await message.answer(f"Подтвердите: отчёт {data['type']} с параметрами {data['params']}? (да/нет)")
    await ReportScenario.waiting_for_confirm.set()

@dp.message_handler(state=ReportScenario.waiting_for_confirm)
async def process_confirm(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        data = await state.get_data()
        await message.answer('Отчёт формируется...')
        # Здесь — вызов LLM или аналитики
    else:
        await message.answer('Сценарий отменён.')
    await state.finish()
