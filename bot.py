import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context  import FSMContext
from aiogram.fsm.state  import StatesGroup, State
from datetime import datetime

Pinkod1 = "2006"
Balans = 1000000
TOKEN = '7652415235:AAHjDacReM5j6SZ9WXFfk_K3xDADaMw-HRI'

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💸Balans💸"), KeyboardButton(text="💰O'tkazmalar💰")]
    ],
    resize_keyboard=True
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Qo'llab-quvvatlash", url="https://t.me/RM_Programmer006")
        ],
        [
            InlineKeyboardButton(text="Like 👍", callback_data="like"), InlineKeyboardButton(text="Dislike 👎", callback_data="dislike")
        ]
    ]
)

class Form(StatesGroup):
    own_card_balans = State()
    own_card_operation = State()
    new_card = State()
    parol1 = State()
    parol2= State()
    mablag = State()

@router.message(CommandStart())
async def start(message: Message):
    
    await message.answer(
        f"Salom {message.from_user.full_name}!\nQuyidagi tugmalardan birini tanlang:",
        reply_markup=reply_kb
    ) 
    await message.answer(
        "Faoliyatimizga o'z xissangizni qo'shing",
        reply_markup=inline_keyboard
    )

@router.callback_query(lambda callback_query: callback_query.data in ["like", "dislike"])
async def handle_inline_buttons(callback_query: CallbackQuery):
    if callback_query.data == "like":
        await callback_query.message.answer("Fikringiz uchun raxmat")
    elif callback_query.data == "dislike":
        await callback_query.message.answer("Fikringiz uchun raxmat")
  
    await callback_query.answer()

@router.message(lambda message : message.text == "💸Balans💸")
async def balans(message: Message, state: FSMContext):
    
    await message.answer("Karta raqamini kiriting:")
    await state.set_state(Form.own_card_balans)

@router.message(Form.own_card_balans)
async def card_balans(message: Message, state: FSMContext):
    
    own_card_number = message.text

    if len(own_card_number) == 16  and own_card_number.isdigit():
        await state.update_data(own_card_number=own_card_number)
        await message.answer("Parolingizni kiriting:")
        await state.set_state(Form.parol1)
    else:
        await message.answer("Karta raqami noto'g'ri kiritildi. Iltimos qaytadan kiriting:")

@router.message(Form.parol1)
async def parol(message: Message, state: FSMContext):
    global Balans
    Pinkod2 = message.text

    if Pinkod2 == Pinkod1:
        await message.answer(f"Sizning balansingiz : {Balans} so'm\n")
        await state.clear()
    else:
        await message.answer("Parolingiz xato! Iltimos qaytadan kiriting:")
        await state.set_state(Form.parol1)

@router.message(lambda message: message.text == "💰O'tkazmalar💰")
async def otkazmalar(message: Message, state: FSMContext):
    
    await message.answer("Iltimos kartangizni kiriting:")
    await state.set_state(Form.own_card_operation)

@router.message(Form.own_card_operation)
async def card_operation(message: Message, state: FSMContext):

    own_card_number = message.text

    if len(own_card_number) == 16 and own_card_number.isdigit():
        await state.update_data(own_card_number=own_card_number)
        await message.answer("Parolingizni kiriting:")
        await state.set_state(Form.parol2)
    else:
        await message.answer("Karta raqami noto'g'ri kiritildi. Iltimos qaytadan kiriting")
        await state.set_state(Form.own_card_operation)

@router.message(Form.parol2)
async def parol(message: Message, state: FSMContext):
    
    Pinkod2 = message.text

    if Pinkod2 == Pinkod1:
        await message.answer("Pul o'tkazmoqchi bo'lgan karta raqamini kiriting:")
        await state.set_state(Form.new_card)
    else: 
        await message.answer("Parolingiz xato! Iltimos qaytadan kiriting:")
        await state.set_state(Form.parol2)

@router.message(Form.new_card)
async def new_card(message: Message, state: FSMContext):

    new_card_number = message.text

    if len(new_card_number) == 16 and new_card_number.isdigit():
        await state.update_data(new_card_number=new_card_number)
        await message.answer("O'tkazmoqchi bo'lgan mablag'ni kiriting:")
        await state.set_state(Form.mablag)
    else:
        await message.answer("Karta raqami noto'gri kiritildi. Iltimos qaytadan kiriting:")
        await state.set_state(Form.new_card)

@router.message(Form.mablag)
async def mablag(message: Message, state: FSMContext):

    global Balans

    try: 
        new_mablag = float(message.text)

        if new_mablag > 0 and new_mablag < Balans:
            Balans -= new_mablag
            await message.answer(f"Pullar muvaffaqiyatli o'tkazildi.\n Sizning balansingiz : {Balans} so'm")
            
            joriy_vaqt = datetime.now()
            sana_text = f"Sana: {joriy_vaqt:%Y-%m-%d %H:%M:%S}"
            user_data = await state.get_data()
            new_card_number = user_data.get("new_card_number")
            own_card_number = user_data.get("own_card_number")
            
            await message.answer(
                f"{sana_text}\n"
                "To'lov kodi: 0ed30655-b8c3-4237-982a-017399f129ac\n"
                f"Qabul qiluvchining kartasi: {new_card_number}\n"
                f"Summa: {new_mablag}\n"
                f"Yuboruvchining FISH: {message.from_user.full_name}\n"
                f"Yuboruvchining kartasi: {own_card_number}"
            )
            await state.clear()
        else:
            await message.answer("Noto'g'ri mablag' kiritildi. Iltimos qaytadan kiriting:")
            await state.set_state(Form.mablag)
    except ValueError:
        await message.answer("Iltimos mablag' to'g'ri raqam sifatida kiriting.")
        await state.set_state(Form.mablag)

dp.include_router(router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())