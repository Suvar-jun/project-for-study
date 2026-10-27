# Сервис-календарь учета рабочего времени и расчета зарплаты.

Сервис позволяет определить рабочий ли сегодня день. Также есть функция трекера для учета отработанного времени.
По итогам отработки рабочего дня можно рассчитать заработную плату.

## Подготовка

### Клонирование репозитория

```bash
git clone https://github.com/andolgov/project-for-study.git
cd project-for-study
```

### Создание виртуального окружения

Перед запуском необходимо создать хранилище секретов в файле .env . Примеры заполнения можно взять из файла .env.example.

Затем необходим создать виртуальное окружение и установить зависимости с помощью команд ниже:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Переменные окружения

Приложение читает настройки из переменных окружения. Если переменная не задана — используется значение по умолчанию.

| Переменная | По умолчанию | Описание |
|---|---|---|
| `APP_NAME` | `HSE Document Finder` | Название приложения — в Swagger UI и логах |
| `APP_VERSION` | `1.0.2` | Версия приложения — в `/version` и в Swagger UI |
| `LOG_LEVEL` | `INFO` | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

## Запуск

```bash
python3 -m uvicorn application:app --host localhost --port 8000
```

После запуска:

- приложение: http://localhost:8000
- документация: http://localhost:8000/docs

## Запуск тестов

```bash
python3 -m pytest -v
```

## Проверка по мере реализации

```bash
curl http://localhost:8000/
```

Проверка "здоровья" приложения:
```bash
curl http://localhost:8000/health
```

Определение текущего дня как рабочего или выходного:
```bash
curl http://localhost:8000/check_workday
```

Запуск трекинга рабочего дня:
```bash
curl http://localhost:8000/start_time
```

Завершения трекинга рабочего дня:
```bash
curl http://localhost:8000/end_time
```

Возвращает текущую версию приложения (значение переменной `APP_VERSION`):
```bash
curl http://127.0.0.1:8000/version
```

### Логи

Все логи пишутся в **stdout** — в терминал, из которого запущен `uvicorn`.

При каждом запросе логируется:
- входящий HTTP-метод и путь
- бизнес-описание вызванного севриса
- какой статус-код отдан клиенту.

Пример:
INFO:     127.0.0.1:56112 - "GET /check_workday HTTP/1.1" 200 OK
2026-10-27 18:59:01,057 INFO application.py Запущена проверка на рабочий или выходной день: app name = СЕРВИС ПРОВЕРКИ РАБОЧЕГО ВРЕМЕНИ, version = 1.0.1


## Диагностика проблем

### `ModuleNotFoundError: No module named 'fastapi'`

Не активировано виртуальное окружение или не установлены зависимости в активированном вирутальном окружении.

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### `ERROR: [Errno 98] error while attempting to bind on address ('127.0.0.1', 8000): address already in use` — порт 8000 занят

Остановите старый сервер (`Ctrl+C`) или запустите новый экземпляр приложения на другом порту:

```bash
python3 -m uvicorn application:app --host localhost --port 8001
```

### DEBUG-логи не появляются

Нужно задать переменную окружения LOG_LEVEL в .env


### `curl: (7) Failed to connect to localhost:8000 after 0 ms: Could not connect to server'

Приложение не запущено. Перезапустите сервис командой и убедитесь в этом, исполнив:

```bash
ps -auxf | grep [a]pplication
```