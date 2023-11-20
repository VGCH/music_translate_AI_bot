## ИИ Телеграм Бот для распознавания текста в музыкальных аудиофайлах и перевода на русский язык
### AI Telegram bot for recognizing and translating song lyrics from an audio file

Бот работает на следующих моделях:

> Whisper от OpenAI

> Helsinki-NLP от Группы исследований языковых технологий Хельсинкского университета.

Для работы бота необходимо установить следующие зависимости/пакеты:
Набор библиотек FFmpeg:
```no-highlight
sudo apt install ffmpeg
```
Менеджер пакетов:
```no-highlight
sudo apt install python3-pip
```

Пакеты Python3:
```no-highlight
pip install transformers, torch, accelerate, sentencepiece, sacremoses, python-telegram-bot, openai-whisper, pydub
```

Команда запуска бота:
```no-highlight
python3 tg_bot.py
```

Полное описание в статье на Хабр

[Ссылка на статью ](https://habr.com/ru/articles/774806/)
