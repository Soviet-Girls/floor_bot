# Бот для вывода флора коллекции в чатик

import os
import random

from dotenv import load_dotenv
from typing import Tuple

from vkbottle import GroupEventType, ABCRule
from vkbottle.bot import Bot, Message, MessageEvent
from vkbottle.tools import PhotoMessageUploader

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import floor
import keyboards
import admin
import chart


bot = Bot(token=os.getenv("VK_API_KEY"))
uploader = PhotoMessageUploader(bot.api, generate_attachment_strings=True)


# Правило для команды
class CommandRule(ABCRule):
    def __init__(self, commands: Tuple[str, ...]):
        self.commands = commands

    async def check(self, message: Message) -> bool:
        return message.text.lower().split()[0] in self.commands

# Вывести актуальный флор
@bot.on.message(CommandRule(commands=("/floor", "/флор")))
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


# Если вступили в закрытый чат по ссылке то обновить ссылку на беседу
@bot.on.chat_invite()
async def chat_invite_handler(message: Message):
    if message.action.type == 'chat_invite_user_by_link' \
        and message.peer_id == 2000000004:
        await bot.api.messages.get_invite_link(peer_id=2000000004, reset=1)

if __name__ == "__main__":
    bot.run_forever()
