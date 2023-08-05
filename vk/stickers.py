import random

# TEMPORARY MOCK DATA
from vk.mock_data import stickers

# TODO:
# - get stickers data from vk api on startup


def get_sticker(word) -> int | None:
    for sticker in stickers["response"]["dictionary"]:
        if word in sticker["words"]:
            return random.choice(sticker["stickers"])["sticker_id"]
    return None


def get_keyword(sticker_id) -> str | None:
    for o in stickers["response"]["dictionary"]:
        for sticker in o["stickers"]:
            if sticker["sticker_id"] == sticker_id:
                return o["words"][0]
    return None
