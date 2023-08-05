# Разнообразим общение в чате нейросеткой от Сбера

import aiohttp

sber_url = 'https://api.aicloud.sbercloud.ru/public/v2/boltalka/predict'

context = {}

def format_response(text: str) -> str:
    text = text.replace("%bot_name", "Анастатия")
    return text

async def get_answer(text: str, peer_id: int):
    try:
        context[str(peer_id)].append(text)
    except KeyError:
        context[str(peer_id)] = [text]

    data = {"instances": [{"contexts": [context[str(peer_id)]]}]}
    headers = {'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.post(sber_url, json=data, headers=headers) as resp:
            response = await resp.json()
            answer = response['responses'].split("['")[1].split("']")[0]

    answer = format_response(answer)
    context[str(peer_id)].append(answer)
    # оставить только 10 последних сообщений в контексте
    context[str(peer_id)] = context[str(peer_id)][-10:]
    return answer