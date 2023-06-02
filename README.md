# Rarible Floor Bot

Rarible Floor Bot — это удобный и функциональный бот, который автоматически обновляет и сообщает актуальный «флор» (минимальную цену) для выбранной коллекции в беседе ВКонтакте.

## Установка

### Bare Metal
1. Клонируйте этот репозиторий.
2. Создайте виртуальное окружение и активируйте его:
```sh
python -m venv venv
. ./venv/bin/activate     # Unix
.\venv\Scripts\activate   # Windows
```

3. Установите необходимые зависимости:
```sh
pip install -r requirements.txt
```

Переименуйте файл `example.env` в `.env` и замените переменные.

4. Для запуска бота используйте следующую команду:
```sh
python main.py
```

### Docker

```sh
docker run -d --name myColl_rfb \
    -e COLLECTION_NAME="Collection Name" \
    -e MARKET_RARIBLE="https://rarible.com/yourcollection" \
    -e MARKET_OPENSEA="https://opensea.io/collection/yourcollection" \
    -e MARKET_OTHER="https://othermarket.com/yourcollection" \
    -e API_RARIBLE="https://api.rarible.org/v/data/collections/NET:COLLECTION/floorPrice/?currency=CUR" \
    -e VK_TOKEN="your-vk-token" \
    -e VK_ADMINS=1234,5678 \
    ghcr.io/steio-labs/rarible_floor_bot:latest
```

### Docker Compose

```yaml
# docker-compose.rfb.yaml
version: "3.8"
services:
  bot:
    image: ghcr.io/steio-labs/rarible_floor_bot:latest
    restart: unless-stopped
    environment:
      - COLLECTION_NAME=<Collection Name>
      - MARKET_RARIBLE=<https://rarible.com/yourcollection>
      - MARKET_OPENSEA=<https://opensea.io/collection/yourcollection>
      - MARKET_OTHER=<https://othermarket.com/yourcollection>
      - API_RARIBLE=<your-api-link>
      - VK_TOKEN=<your-vk-token>
      - VK_ADMINS=<admin-id-1>,<admin-id-2>
```

```sh
docker compose up -d
```

## Переменные окружения

| Name                 | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `COLLECTION_NAME`    | Имя коллекции для отображения на графике. По умолчанию *КриптоКоллекция* |
| `MARKET_RARIBLE`     | Ссылка на маркет rarible. Может быть пустым                  |
| `MARKET_OPENSEA`     | Ссылка на маркет opensea. Может быть пустым                  |
| `MARKET_OTHER`       | Ссылка на внешнюю маркет-платформу. Может быть пустым        |
| `API_RARIBLE`        | Ссылка на API RARIBLE с указанием коллекции                  |
| `API_COINBASE`       | Ссылка на API COINBASE. Рекомендуется значение по умолчанию  |
| `VK_TOKEN`           | Токен от группы ВКонтакте                                    |
| `VK_ADMINS`          | ID админов бота, которые могут не являться администраторами чата (список) |

- `API_RARIBLE` ссылка формируется по следующему правилу `https://api.rarible.org/v0.1/data/collections/` + **`СЕТЬ:`** + **`адрес коллекции в сети Polygon`** + `/floorPrice/?currency=` + **`ТОКЕН`**. В таком случае для сети [Polygon](https://polygon.technology) и коллекции [CryptoSpotty](https://rarible.com/Cryptospotty) ссылка будет выглядеть так: `https://api.rarible.org/v0.1/data/collections/POLYGON:0x0ad52bfd0ddd09f581f0f790fe4f7369e9097712/floorPrice/?currency=MATIC`



## Использование
Бот поддерживает следующие команды:

### Пользовательские команды
- `/флор` или `/floor` — получить актуальный флор коллекции.

## TODO
- [ ] Добавить рассылку по таймеру
- [ ] Добавление нескольких коллекций
- [ ] Добавить настройки внутри бота
- [ ] Определять редкость NFT из коллекции по ссылке rarible или opensea
- [x] Добаить курс валюты MATIC к рублю и доллару
- [ ] Повесить обработчик ошибок на модуль курса валют
