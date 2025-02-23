from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.reply_keyboards import kb_back

keyboard_router = Router()


@keyboard_router.message(F.text == 'ChatGPT')
async def kb_chatgpt(message: Message):
    await message.answer(
        text='Скоро тут появится ChatGPT',
        reply_markup=kb_back(),
    )


@keyboard_router.message(Command('random'))
@keyboard_router.message(F.text == 'Случайный факт')
async def kb_random(message: Message):
    await message.answer(
        text='Случайный факт',
        reply_markup=kb_back(),
    )
