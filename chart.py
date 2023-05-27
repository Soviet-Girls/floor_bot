# Генератор графиков

import io
import seaborn

def generate(data: dict) -> bytes:
    # Превращаем даты в данных из 2023-04-25 в 25.04.2023
    data["historicalDates"] = [
        date.split("-")[2] + "." + date.split("-")[1]
        for date in data["historicalDates"]
    ]
    # Генерируем график за последние 6 дней
    data["historicalDates"] = data["historicalDates"][-6:]
    data["historicalValues"] = data["historicalValues"][-6:]
    seaborn.set_theme(style="darkgrid")
    c = seaborn.lineplot(
        data=data,
        x="historicalDates",
        y="historicalValues",
    )
    # Настраиваем график
    c.set_title("График флора Soviet Girls", fontsize=16)
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
