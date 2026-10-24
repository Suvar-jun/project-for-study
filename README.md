# FastAPI: реализуем приложение вместе

Главный файл — `application.py`. 

## Подготовка

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Запуск

```bash
python3 -m uvicorn application:app --host localhost --port 8000
```

После запуска:

- приложение: http://localhost:8000
- документация: http://localhost:8000/docs

## Проверка по мере реализации

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl "http://localhost:8000/hello?name=Alexey"
```

Перед последним шагом задайте настройки и перезапустите сервер:

```bash
export APP_NAME="Проект группы 1"
export APP_AUTHOR="Иван Иванов"
python3 -m uvicorn application:app --host localhost --port 8000
```

Проверка:

```bash
curl http:/localhost:8000/info
```
