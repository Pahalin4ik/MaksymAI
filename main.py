import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from openai import AsyncOpenAI


class Dialog(StatesGroup):
    dialog = State()


api_key = os.getenv("APIKEY")
client = AsyncOpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
dp = Dispatcher()


@dp.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.set_state(Dialog.dialog)
    await state.set_data({"dialog": [{"role":"system", "content": "Розмовляй, як маніяк"}]})
    await msg.answer("Привіт, я максим і я не маніяк")


@dp.message(Command("exit"))
async def exit():
    await dp.stop_polling()


@dp.message()
async def messages(msg: Message, state: FSMContext):
    dialog: list[dict[str, str]] = (await state.get_data())['dialog']
    dialog.append({"role": "user", "content": msg.text})
    completion = await client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=dialog,
        stream=False
    )
    dialog.append({"role": "assistant", "content": completion.choices[0].message.content})
    await state.set_data({"dialog": dialog})
    await msg.answer(completion.choices[0].message.content)


async def main() -> None:
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
