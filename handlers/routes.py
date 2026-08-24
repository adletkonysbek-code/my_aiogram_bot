import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.keys import get_keyboard, get_inline, get_new_inline
from aiogram.enums import ChatMemberStatus
from config import bot

CHANNEL_ID = -1004471778918
CHANNEL_ID2 = -1003901159522


router = Router()
stories_queue = []


async def check_sub(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
    except Exception as e:
        logging.error(f"Ошибка проверки подписки: {e}")
        return False

class form(StatesGroup):
    gender = State()
    age = State()
    history = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "⚠️<b>Перед тем как записать свою историю прочитайте!</b>\n"
        "❗️1. Запишите историю, правильно расставив запятые и точки.\n"
        "❗️2. Используйте эмодзи умеренно, не добавляйте их к каждому слову или предложению.\n"
        "❗️3. Если вы столкнулись с ситуацией, похожей на ту, о которой читали в этой группе, писать об этом не нужно.\n"
        "❗️4. Все события будут отложены на 4–5 дней (а возможно, и на более долгий срок)!\n"
        "<b>ВСЕ БУДЕТ АНОНИМНО</b>\n\n"
        "<b>Сначал подпишитесь на канал снизу!</b>\n"
        f'<a href="https://t.me/pozornikistorya">• ПОДПИСАТЬСЯ</a>'
    )

    await message.answer(text, parse_mode="HTML", reply_markup=get_keyboard())
    await message.answer("Выберите Пол:")

    

@router.message(F.text.in_({"Мужчина", "Женщина"}) )
async def process_gender(message: Message, state: FSMContext):

    if not await check_sub(bot, message.from_user.id):
        await message.answer(f"Сначала подпишитесь на канал!❌")
        return

    await state.update_data(gender=message.text)

    await message.answer("Отлично!\nТеперь введите ваш возраст:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(form.age)


@router.message(form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом")
        return

    if int(message.text) < 14 or int(message.text) > 41:
        await message.answer("Возраст должен быть от 14 до 40!")
        return

    await state.update_data(age=int(message.text))

    await message.answer("Отлично!\nТеперь запишите вашу историю:")
    await state.set_state(form.history)


@router.message(form.history, F.text)
async def process_history(message: Message, state: FSMContext):
    await message.answer(
        "Спасибо за вашу историю!❤️🚀",
        reply_markup=get_inline()
    )
    await state.update_data(history=message.text)


@router.callback_query(F.data == "new_history")
async def cmd_new(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await cmd_start(callback.message)
    await state.clear()


@router.callback_query(F.data == "cmd_otpravit")
async def cmd_historyot(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gender = data["gender"]
    age = data["age"]
    history = data["history"]

    text = f"<b>{gender[0]}{age}</b>. {history}\n\n"
    "<a href='https://t.me/pozornikistorya'>ПОЗОРНИКИ</a>"

    stories_queue.append(text)

    await callback.message.answer("✅ Ваша история добавлена в очередь и скоро будет опубликована в канале!", reply_markup=get_new_inline())
    await callback.answer()


async def send_story_to_channel(bot: Bot):
    if stories_queue:

        story_text = stories_queue.pop(0) 
        
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID2,
                text=story_text,
                parse_mode="HTML"
            )
            
            print("История успешно отправлена в канал!")
        except Exception as e:
            print(f"Ошибка при отправке в канал: {e}")
    else:
        print("Очередь историй пуста, отправлять нечего.")