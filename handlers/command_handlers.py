import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import kb_start, kb_back, ikb_celebrity, ikb_select_subject_quiz
from keyboards.callback_data import QuizData
from fsm.states import ChatGPTStates

command_router = Router()


@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
@command_router.message(F.text == 'Закончить')
@command_router.callback_query(QuizData.filter(F.subject == 'quiz_back'))
async def com_start(message: Message | CallbackQuery, state: FSMContext):
    if isinstance(message, Message):
        await message.answer_photo(
            photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
            caption=f'Привет, {message.from_user.full_name}!',
            reply_markup=kb_start(),
        )
    else:
        await message.bot.send_photo(
            chat_id=message.from_user.id,
            photo=FSInputFile(path=os.path.join('images', 'main.jpg')),
            caption=f'Привет, {message.from_user.full_name}!',
            reply_markup=kb_start(),
        )
        await state.clear()


@command_router.message(F.text == 'Помощь')
@command_router.message(Command('help'))
async def com_help(message: Message):
    await message.answer(
        text='Привет! Этот бот совмещает с себе удобство _Telegram_ и мощь *ChatGPT*\n\n'
             '*Полезные команды и ссылки:*\n'
            '1. /start — главное меню бота\n'
            '2. /random - узнать рандомный факт · 🧠\n'
            '3. /gpt - Задать вопрос ChatGPT · 🤖\n'
            '4. /talk - поговорить с известной личностью · 👤\n'
            '5. /quiz - проверить свои знания ❓',
        reply_markup=kb_back(),
    )


@command_router.message(Command('gpt'))
async def ai_gpt_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'gpt.jpg'))
    # for item in dict(completion).items():
    #     print(item)
    await message.answer_photo(
        photo=photo_file,
        caption='Напишите запрос к ChatGPT',
        reply_markup=kb_back(),
    )
    await  state.set_state(ChatGPTStates.wait_for_request)


@command_router.message(F.text == 'Диалог с личностью')
@command_router.message(Command('talk'))
async def talk_command(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'talk.jpg'))
    await message.answer_photo(
        photo=photo_file,
        caption='Выберите, с кем вы хотите поговорить',
        reply_markup=ikb_celebrity(),
    )
    await  state.set_state(ChatGPTStates.wait_for_request)


@command_router.callback_query(QuizData.filter(F.button == 'select_type'))
@command_router.message(F.text == 'Квиз')
@command_router.message(Command('quiz'))
async def quiz_select_subject(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join('images', 'quiz.jpg'))
    await message.bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo_file,
        caption='Выберите тему вопросов:',
        reply_markup=ikb_select_subject_quiz(),
    )
