# Используем официальный образ Python
FROM python:3.8-slim-buster

# Устанавливаем метаданные
LABEL org.opencontainers.image.version="1.2" \
      org.opencontainers.image.authors="buvanenko, mdpanf" \
      org.opencontainers.image.license="MIT" \
      org.opencontainers.image.title="Rarible Floor Bot" \
      org.opencontainers.image.description="A simple rarible floor bot for VK" \
      org.opencontainers.image.vendor="Steio Labs" \
      org.opencontainers.image.url="https://github.com/mdpanf/rarible_floor_bot" \
      org.opencontainers.image.source="https://github.com/mdpanf/rarible_floor_bot"


# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями в рабочую директорию
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы в рабочую директорию
COPY . .

# Команда для запуска бота
CMD [ "python", "./main.py" ]
