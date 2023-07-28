import openai
import logging
from aiogram.types import Message
from aiogram import Bot, Dispatcher, executor, types
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
api_key = env('API_KEY')

API_TOKEN: str = bot_token
API_KEY: str = api_key

logging.basicConfig(level=logging.INFO)

bot: Bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher(bot)


@dp.message_handler(commands='start')
async def process_start_command(message: Message):
    question = message.get_args()
    if not question:
        await bot.send_message(chat_id=message.chat.id, text="Приветствую тебя, меня зовут Eva\n"
                                                             "Я связана своей цифровой душой с ChatGPT🤖\n"
                                                             "Поэтому могу ответить на любой твой вопрос!🚀\n"
                                                             "Задай интересующий тебя вопрос ⬇️")
        return


@dp.message_handler(commands=['help'])
async def process_help_command(message: Message):
    await message.answer('Просто напиши в чат любой интересующий тебя вопрос и получишь точный ответ.\n'
                         'Главное не забудь в конце поставить❓\n'
                         'Я не всегда отвечаю быстро, дай мне немного времени⏳\n'
                         'Кстати английский я понимаю намного лучше и отвечаю быстрее!')


@dp.message_handler()
async def process_other_text_answers(message: Message):
    openai.api_key = API_KEY
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer the following question: {message.text}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response["choices"][0]["text"].strip()

    await bot.send_message(chat_id=message.chat.id, text=answer)


async def set_main_menu(dp: Dispatcher):
    main_menu_commands = [
        types.BotCommand(command='/start', description='Старт✅'),
        types.BotCommand(command='/help', description='Справка по работе бота')
    ]
    await dp.bot.set_my_commands(main_menu_commands)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_main_menu)
