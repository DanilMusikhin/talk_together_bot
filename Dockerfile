# Официальный образ питона
FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y build-essential

# Установка рабочей директории
WORKDIR /app

# Создание папки для бд
RUN mkdir -p /app/db

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Указываем переменные окружения (можно переопределить в docker-compose)
ENV PYTHONNONBUFFERED=1

# Запуск бота
CMD ["python", "bot.py"]
