# Бот для вывода флора коллекции в чатик

import os
import asyncio
import random

from dotenv import load_dotenv
from typing import Tuple


from vkbottle import GroupEventType
from vkbottle.bot import Bot, Message, MessageEvent
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.tools import PhotoMessageUploader

import floor
import keyboards
import admin
import chart
import dialogue
from rules import ChitChatRule

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


bot = Bot(token=os.getenv("VK_API_KEY"))
uploader = PhotoMessageUploader(bot.api, generate_attachment_strings=True)

schedule_peer_id = 0


# Вывести актуальный флор
@bot.on.message(text="/флор")
async def now_handler(message: Message):
    bot_message = await floor.get()
    if message.peer_id == message.from_id:
        raw_data = await floor.get_raw()
        buf = chart.generate(raw_data)
        attachment = await uploader.upload(buf, peer_id=message.peer_id)
        await message.answer(
            bot_message, attachment=attachment, keyboard=keyboards.market_links
        )
    else:
        is_admin = await admin.check(bot, message.peer_id, message.from_id)
        if is_admin == False:
            await message.answer("У вас нет доступа к этой команде")
            return
        await message.answer(bot_message, keyboard=keyboards.market_links_conversation)


# Отправлять флор каждые n минут
@bot.on.message(CommandRule("старт", ["/"], 1))
async def schedule_handler(message: Message, args: Tuple[str]):
    is_admin = await admin.check(bot, message.peer_id, message.from_id)
    if is_admin == False:
        await message.answer("У вас нет доступа к этой команде")
        return
    global schedule_peer_id  # позор мне за глобальную переменную
    if schedule_peer_id == message.peer_id:
        await message.answer("Бот уже запущен")
        return
    schedule_peer_id = message.peer_id
    while schedule_peer_id == message.peer_id:
        bot_message = await floor.get()
        await message.answer(bot_message, keyboard=keyboards.market_links_conversation)
        await asyncio.sleep(int(args[0]) * 60)


# Остановить отправку флора
@bot.on.message(text="/стоп")
async def stop_handler(message: Message):
    is_admin = await admin.check(bot, message.peer_id, message.from_id)
    if is_admin == False:
        await message.answer("У вас нет доступа к этой команде")
        return
    global schedule_peer_id
    schedule_peer_id = 0
    await message.answer("Бот остановлен")

# Обработка callback
@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def chart_handler(event: MessageEvent):
    print(event.object.payload)
    
    # Обновить флор в сообщении
    if event.object.payload.get("command") == "update":
        bot_message = await floor.get()
        await bot.api.messages.edit(
            peer_id=event.object.peer_id,
            conversation_message_id=event.conversation_message_id,
            message=bot_message,
            keyboard=keyboards.market_links_conversation,
        )
        await event.show_snackbar("Флор обновлен!")
        return
    
    # Обновить флор в личных сообщениях
    if event.object.payload.get("command") == "update_full":
        bot_message = await floor.get()
        raw_data = await floor.get_raw()
        buf = chart.generate(raw_data)
        attachment = await uploader.upload(buf, peer_id=event.object.peer_id)
        await bot.api.messages.edit(
            peer_id=event.object.peer_id,
            conversation_message_id=event.conversation_message_id,
            message=bot_message,
            attachment=attachment,
            keyboard=keyboards.market_links,
        )
        await event.show_snackbar("Флор обновлен!")
        return

    raw_data = await floor.get_raw()
    buf = chart.generate(raw_data)
    try:
        attachment = await uploader.upload(buf, peer_id=event.object.user_id)
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            attachment=attachment,
            keyboard=keyboards.market_links,
            random_id=random.randint(0, 2 ** 64),
        )
        await event.show_snackbar("График отправлен в личные сообщения!")
        return
    except Exception as e:
        await event.show_snackbar("Не удалось отправить график! Возможно, у вас нет диалога с ботом.")
        raise e

# Проверка на права администратора
@bot.on.message(text="/admin")
async def admin_handler(message: Message):
    is_admin = await admin.check(bot, message.peer_id, message.from_id)
    if is_admin == False:
        await message.answer("У вас нет доступа к этой команде")
        return
    await message.answer("Вы администратор")

# Болталка
@bot.on.message(ChitChatRule())
async def chit_chat_handler(message: Message):
    bot_message = await dialogue.get_answer(message.text, message.peer_id)
    await message.answer(bot_message)
    
if __name__ == "__main__":
    bot.run_forever()
