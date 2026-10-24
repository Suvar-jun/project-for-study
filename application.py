"""Итоговый вариант приложения для преподавателя и сверки."""

import os

from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import date, datetime, timezone

app = FastAPI(title="Сервис проверки рабочего времени")
load_dotenv()
start_time = None

@app.get("/")
def root():
    return {"message": "Сервис работает"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello(name: str = "студент"):
    return {"message": f"Привет, {name}!"}


@app.get("/info")
def info():
    app_name = os.getenv("APP_NAME", "Учебный сервис")
    app_author = os.getenv("APP_AUTHOR", "Не указан")

    return {
        "app_name": app_name,
        "author": app_author,
    }

@app.get("/check_workday")
def check_workday():
    today = date.today()
    # weekday() возвращает 0 для понедельника, 6 для воскресенья
    if today.weekday() >= 5:  # 5 — суббота, 6 — воскресенье
        return "Сегодня выходной день, время трекать не нужно!"
    else:
        return ("Сегодня рабочий день, запустите учет начала рабочего дня, "
                "вызвав эндпоинт /start_time. По завершении рабочего дня вызовите /end_time, "
                "чтобы получить отработанное за сегодня время в часах и минутах.")

@app.get("/start_time")
def start_time_endpoint():
    global start_time
    start_time = datetime.now(timezone.utc)  # лучше хранить в UTC
    return {
        "status": "started",
        "start_time": start_time.isoformat(),
        "message": f"Отчёт времени пошёл. Начало работы в {start_time.strftime('%H:%M:%S')}"
    }

@app.get("/end_time")
def end_time_endpoint():
    global start_time
    if start_time is None:
        return {
            "status": "error",
            "message": "Сначала запустите /start_time"
        }

    end_time = datetime.now(timezone.utc)
    duration = end_time - start_time  # timedelta

    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    # Сбрасываем, чтобы нельзя было дважды посчитать без нового старта
    start_time = None

    return {
        "status": "finished",
        "end_time": end_time.isoformat(),
        "duration_hours": hours,
        "duration_minutes": minutes,
        "message": f"Рабочий день завершён. Отработано: {hours} ч {minutes} мин"
    }