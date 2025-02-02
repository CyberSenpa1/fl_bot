from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.start_kb import get_choose
from db.users import User

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет, {message.from_user.first_name}',
        reply_markup=get_choose(),
    )
    # Call create_user with 'await' for async handling
    await User.create_user(message.from_user.id, message.from_user.full_name)
