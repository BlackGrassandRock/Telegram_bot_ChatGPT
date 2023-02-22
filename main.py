import os
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import * #secure data


bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)

class Gpt():

    def __init__(self, user_name, txt_message):
        self._user = str(user_name)
        self.prompt = str(txt_message)

    def validator(self):
        if self.prompt[0:4] == "bot ":
            return True

    def interaction_gpt(self):
        self.prompt = self.prompt[4:] #cut phrase "bot "
        openai.api_key = AI_KEY

        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        return completion.choices[0].text

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hi. This is a bot for communication with ChaGPT. If you want to ask AI any question, Start your conversation with the phrase 'bot ...'.")

@dp.message_handler()
async def echo_message(msg: types.Message):
    tg_user = Gpt(msg.from_user.username, msg.text)
    if tg_user.validator():
        await bot.send_message(msg.from_user.id, tg_user.interaction_gpt())

if __name__ == '__main__':
    executor.start_polling(dp)
