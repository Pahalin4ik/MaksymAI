from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("APIKEY"), base_url="https://openrouter.ai/api/v1")


async def ask(dialog: list[dict[str, str]], message: str, file_id: str | None = None):
    dialog.append({"role": "user", "content": message})
    while True:
        completion = await client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=dialog,
            stream=False
        )
        if completion.choices:
            dialog.append({"role": "assistant", "content": completion.choices[0].message.content})
            return dialog, completion.choices[0].message.content

