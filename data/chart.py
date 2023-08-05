# -*- coding: utf-8 -*-
# Построение графика

# Импорт необходимых модулей
import io
import seaborn
import datetime
from config import config

def generate(data: dict) -> bytes:
    # Превращаем даты в данных из 2023-04-25 в 25.04
    data["historicalDates"] = [
        datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m') 
        for date in data["historicalDates"]
    ]
    # Генерируем график за последние 7 дней
    data["historicalDates"] = data["historicalDates"][-7:]
    data["historicalValues"] = data["historicalValues"][-6:]
    data["historicalValues"].append(data["currentValue"])
    seaborn.set_theme(style="darkgrid")
    c = seaborn.lineplot(
        data=data,
        x="historicalDates",
        y="historicalValues",
    )
    # Настраиваем график
    c.set_title(f"График флора {config.nft.name}", fontsize=16)
    c.set_xlabel("")
    c.set_ylabel("Цена в MATIC")
    # Делаем график более широким
    c.figure.set_figwidth(8)
    # Сохраняем график в буфер
    buf = io.BytesIO()
    c.figure.savefig(buf, format="png")
    # Очищаем график
    c.figure.clf()
    # Возвращаем буфер
    buf.seek(0)
    return buf.read()
