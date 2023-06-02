# -*- coding: utf-8 -*-
#!/usr/bin/env python
# PEP-8
# Copyright (C) 2023 buvanenko, mdpanf
# Licensed under https://mit-license.org

# Импорт необходимых модулей
import asyncio
import random

from config import config
from typing import Tuple

from vkbottle import GroupEventType, ABCRule
from vkbottle.bot import Bot, Message, MessageEvent
from vkbottle.tools import PhotoMessageUploader

import floor
import keyboards
import admin
import chart
import widget


bot = Bot(token=config.vk.token)
uploader = PhotoMessageUploader(bot.api, generate_attachment_strings=True)


# Правило для команды
class CommandRule(ABCRule):
    def __init__(self, commands: Tuple[str, ...]):
        self.commands = commands

    async def check(self, message: Message) -> bool:
        return message.text.lower().split()[0] in self.commands


# Вывести актуальный флор
@bot.on.message(CommandRule(commands=("/floor", "/флор", "/akjh", "начать", "start")))
async def now_handler(message: Message):
    bot_message = await floor.get()
    if message.peer_id == message.from_id:
        raw_data = await floor.get_raw()
        buf = chart.generate(raw_data)
        attachment = await uploader.upload(buf, peer_id=message.peer_id)
        await message.answer(
            bot_message, attachment=attachment, keyboard=keyboards.get_dm()
        )
    else:
        if not await admin.check(bot, message.peer_id, message.from_id):
            await message.answer("У вас нет доступа к этой команде")
            return
        await message.answer(bot_message, keyboard=keyboards.get_chat())


# Обработка callback
@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent)
async def chart_handler(event: MessageEvent):
    
    # Обновить флор в сообщении
    if event.object.payload.get("command") == "update":
        bot_message = await floor.get()
        await bot.api.messages.edit(
            peer_id=event.object.peer_id,
            conversation_message_id=event.conversation_message_id,
            message=bot_message,
            keyboard=keyboards.get_chat(),
        )
        await event.show_snackbar("Флор обновлен!")
        return
    
    # Обновить флор в личных сообщениях
    if event.object.payload.get("command") == "full_update":
        bot_message = await floor.get()
        raw_data = await floor.get_raw()
        buf = chart.generate(raw_data)
        attachment = await uploader.upload(buf, peer_id=event.object.peer_id)
        await bot.api.messages.edit(
            peer_id=event.object.peer_id,
            conversation_message_id=event.conversation_message_id,
            message=bot_message,
            attachment=attachment,
            keyboard=keyboards.get_dm(),
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
            keyboard=keyboards.get_dm(),
            random_id=random.randint(0, 2 ** 64),
        )
        await event.show_snackbar("График отправлен в личные сообщения!")
        return
    except Exception as e:
        await event.show_snackbar("Не удалось отправить график! Возможно, у вас нет диалога с ботом.")
        raise e

# Обновлять виджет каждые 5 минут
@bot.loop_wrapper.timer(seconds=5)
async def update_widget():
    await widget.update()
    print("Widget updated")

if __name__ == "__main__":
    bot.run_forever()
