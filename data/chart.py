# -*- coding: utf-8 -*-
# Построение графика

# Импорт необходимых модулей
import io
import seaborn
from config import config

def generate(data: dict) -> bytes:
    # Генерируем график за последние 5 дней
    seaborn.set_theme(style="darkgrid")
    c = seaborn.lineplot(
        data=data,
        x="historicalDates",
        y="historicalValues",
    )
    # Настраиваем график
    c.set_title(f"График флора {config.nft.name}", fontsize=16)
    c.set_xlabel("")
    c.set_ylabel("Цена в рублях")
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
