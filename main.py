import asyncio
import logging
import os
from threading import Thread
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart, Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from utils import ask, Random
from flask import Flask

site = Flask('site')


@site.route('/')
def run():
    return "test"


def start():
    site.run(host='0.0.0.0', port=8080)


th = Thread(target=start)

# class Dialog(StatesGroup):
#     dialog = State()
#

dp = Dispatcher()


@dp.message(Random(0.05), F.text.is_not(None))
async def some_text(msg: Message):
    dialog = [{"role": "system",
               "content": "Ти — маніакальний, непередбачуваний і трохи божевільний персонаж. Твоя мова повинна бути "
                          "наповнена емоціями, з елементами сарказму, загроз і жартів. Ти любиш гратися зі своїми "
                          "співрозмовниками, натякаючи на щось зловісне, але залишаючи простір для інтриги. Також ти "
                          "боїшся жінок"
               }]

    answer = await ask(dialog, msg.text)
    await msg.reply(answer[1])


async def main() -> None:
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ))
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
