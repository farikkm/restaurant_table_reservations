# Структура проекта для `aiogram`

## Шаги для ее инициализации

### 1 Шаг. Склонировать репо
```commandline
git clone ...
```

### 2 Шаг. Установить виртуальное окружение
```commandline
python3 -m venv .venv
```

### 3 Шаг. Активировать виртуальное окружение
- Windows
```commandline
.venv\Scripts\activate.bat
```
- MacOS/Linux (Bash)
```bash
source .venv/bin/activate
```

### 4 Шаг. Установить начальные, необходимые зависимости
```commandline
pip install -U aiogram python-dotenv watchfiles
```

### 5 Шаг. Создать файл .env
```bash
echo "BOT_TOKEN=ТОКЕН_ТВОЕГО_БОТА" > .env
```

### 6 Шаг. Запустить программу
```commandline
watchfiles "python main.py" .
```
