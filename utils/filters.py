from aiogram.filters import Filter
from aiogram.types import Message
from random import random


class Random(Filter):
    def __init__(self, k: float) -> None:
        self.k = k

    async def __call__(self, message: Message) -> bool:
        return random() * (self.k**-1) < 1
