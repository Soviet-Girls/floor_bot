# -*- coding: utf-8 -*-
#!/usr/bin/env python
# PEP-8
# Copyright (C) 2023 buvanenko, mdpanf
# Licensed under https://mit-license.org

# Импорт необходимых модулей
import random
import traceback

from config import config
from typing import Tuple

from vkbottle import GroupEventType, ABCRule
from vkbottle.bot import Bot, Message, MessageEvent
from vkbottle.tools import PhotoMessageUploader
from stories_uploader import StoriesUploader

from data import floor, nft, chart, dialogue, staking, rubles, stories, currency
from vk import keyboards, widget, cleaner, chat_info, stickers

import formating

from vk.rules import ChitChatRule

bot = Bot(token=config.vk.token)
uploader = PhotoMessageUploader(bot.api, generate_attachment_strings=True)
stories_uploader = StoriesUploader(bot.api)


async def post_story():
    try:
        stats = await floor.get_stats()
        matic_rub, matic_usd = await currency.get_matic_rate()
        floor_rub = '{0:,}'.format(int(stats['floorPrice'] * matic_rub)).replace(',', ' ')
        volume_rub = '{0:,}'.format(int(stats['volume'] * matic_rub)).replace(',', ' ')
        image = stories.generate_image(f"{floor_rub} ₽", f"{volume_rub} ₽", stats['owners'], stats['items'])
        attachment = await stories_uploader.upload(image, add_to_news=1, link_text="to_store", link_url="https://vk.com/wall-220643723_72")
        return attachment
    except Exception as e:
        await bot.api.messages.send(
            peer_id=434356505,
            message=traceback.format_exc(),
            random_id=random.randint(0, 2**64),
        )

def generate_reply(ans: Message):
    string = f'"peer_id": {ans.peer_id}, "conversation_message_ids": [{ans.conversation_message_id}], \
        "is_reply": 1'
    return "{" + string + "}"


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
        # if not await admin.check(bot, message.peer_id, message.from_id):
        #     await message.answer("У вас нет доступа к этой команде")
        #     return
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
            random_id=random.randint(0, 2**64),
        )
        await event.show_snackbar("График отправлен в личные сообщения!")
        return
    except Exception as e:
        await event.show_snackbar(
            "Не удалось отправить график! Возможно, у вас нет диалога с ботом."
        )
        raise e


# Получить адрес кошелька
@bot.on.message(CommandRule(commands=("/кошелек", "/кошелёк", "/wallet")))
async def wallet_handler(message: Message):
    address = await bot.api.storage.get("wallet", user_id=message.from_id)
    if address[0].value == "":
        await message.answer("👛 Кошелек не привязан! Посетите auth.sovietgirls.su")
        return

    m = await bot.api.messages.send(
        peer_id=message.peer_id,
        message="👛 Пожалуйста, подождите...",
        random_id=random.randint(0, 2**64),
    )

    balance, balance_matic, balance_rub, balance_usd = await nft.get_balance(
        address[0].value
    )
    sgr_count = await rubles.balance_of(address[0].value)
    bot_message = f"👛 Адрес кошелька: {address[0].value}\n"
    bot_message += f"💳 {sgr_count} SG₽\n\n"
    bot_message += f"👧 NFT на аккаунте: {balance}\n"
    bot_message += "🪙 Цена по флору:\n"
    bot_message += f"MATIC: {balance_matic}\n"
    bot_message += f"Рубли: {balance_rub} ₽\n"
    bot_message += f"Доллары: {balance_usd} $\n\n"

    staking_count = await staking.balance_of(address[0].value)
    if staking_count > 0:
        bot_message += f"⛏️ NFT в стейкинге: {staking_count}\n"
        bot_message += f"({round(staking_count*1.4,2)} SG₽/Час)"

    keyboard = keyboards.get_wallet(address[0].value)

    await bot.api.messages.edit(
        peer_id=message.peer_id,
        message_id=m,
        message=bot_message,
        keyboard=keyboard.get_json(),
    )
    # await message.answer(bot_message, keyboard=keyboard.get_json())

# Запостить историю
@bot.on.message(CommandRule(commands=("/story")))
async def story_handler(message: Message):
    await post_story()
    await message.answer("История успешно опубликована!")


# Принудительная очистка
@bot.on.message(CommandRule(commands=("/clean", "/очистить")))
async def clean_handler(message: Message):
    await cleaner.start(bot=bot)
    await message.answer("Очистка завершена!")


# Болталка
@bot.on.message(ChitChatRule())
async def chit_chat_handler(message: Message):
    address = await bot.api.storage.get("wallet", user_id=message.from_id)
    if address[0].value == "":
        return
    owner = await nft.check_owner(address[0].value)
    if not owner:
        return
    
    user = await bot.api.users.get(user_ids=message.from_id)
    user_name = f"{user[0].first_name}"

    await bot.api.messages.set_activity(type="typing", peer_id=message.peer_id)
    answer = dialogue.get_answer(message.text, message.peer_id, user_name)

    if "OPERATOR_CALL" in answer and message.peer_id == message.from_id:
        await message.answer("👮‍♂️ Оператор вызван!")
        await bot.api.messages.send(
            peer_id=434356505,
            message=f"👮‍♂️ Оператор вызван в чате https://vk.com/gim220643723?sel={message.peer_id}",
            random_id=random.randint(0, 2**64),
        )
        return
    elif "OPERATOR_CALL" in answer:
        await message.answer(
            "Я не могу ответить на этот вопрос. Попробуйте сформулировать его иначе."
        )
        return

    if "FLOOR_CALL" in answer:
        await now_handler(message)
        return
    
    if "WALLET_CALL" in answer:
        await wallet_handler(message)
        return

    if message.peer_id != message.from_id:
        await message.answer(
            formating.remove_emoji(answer), forward=generate_reply(message)
        )
    else:
        await message.answer(formating.remove_emoji(answer))

    emoji = formating.find_emoji(answer)
    if emoji:
        sticker = stickers.get_sticker(emoji)
        if sticker:
            await message.answer("", sticker_id=sticker)


# Выполнять каждую минуту
@bot.loop_wrapper.interval(minutes=1)
async def update():
    try:
        await widget.update()
        await cleaner.start(bot=bot)
        await chat_info.check_stats()
    except Exception as e:
        await bot.api.messages.send(
            peer_id=434356505,
            message=traceback.format_exc(),
            random_id=random.randint(0, 2**64),
        )

# Выполнять каждые сутки
@bot.loop_wrapper.interval(hours=24)
async def daily():
    try:
        await post_story()
    except Exception as e:
        await bot.api.messages.send(
            peer_id=434356505,
            message=traceback.format_exc(),
            random_id=random.randint(0, 2**64),
        )


if __name__ == "__main__":
    bot.run_forever()
