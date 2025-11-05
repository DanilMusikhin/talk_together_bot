# Описание
Данный бот является помощником в создании интересной беседы с помощью выдачи интересных вопросов

# Запуск
### 0. Открываем файл config, вставляем значения, переименовывем в config.env

## Развертывание с помощью Docker
### 1. Собираем и запускаем, или просто запускаем
```cmd
docker compose up -d --build
docker compose up -d
```
### 2. Просмотр логов с момента запуска и в реальном времени
```cmd
docker logs talk-together-bot
docker compose logs -f talk-together-bot
```
### 3. Остановка или перезапуск
```cmd
docker compose down
docker compose restart talk-together-bot
```

## Запуск через питон
### 1. Устанавливаем необходимые зависимости
```cmd
pip install -r requirements.txt
```
### 2. Запускаем
```cmd
python3 bot.py
```