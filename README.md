# DrWeb - Тестовое Задание (Python Backend)

![Screenshot](https://i.imgur.com/Ksb2OA5.png)

## Описание задачи

Этот проект реализует **HTTP API** для хранения и управления файлами. Сервис поддерживает три основных действия: загрузка **(upload)**, скачивание **(download)** и удаление **(delete)** файлов.

## Стек технологий

Технологии, используемые в проекте:

- python 3.11.6
- Flask
- SQLAlchemy
- SQLite
- Docker/docker-compose
- pytest
- gunicorn
- flask-migrate
- poetry

## Функционал

### Upload (POST)

1. Авторизованный пользователь загружает файл.
2. Файл сохраняется на диск в структуре каталогов:
store/ab/abcdef12345...
где "abcdef12345..." - имя файла, совпадающее с его хэшем.
/ab/ - подкаталог, состоящий из первых двух символов хэша файла.
3. Возвращает хэш загруженного файла;

Алгоритм хэширования - **sha256**.

### Delete (DELETE)

1. Авторизованный пользователь передает хэш файла, который необходимо удалить.
2. Если по хэшу файл удалось найти в локальном хранилище и файл принадлежит пользователю, то файл удаляется.

### Download (GET)

1. Любой пользователь передает параметр — хэш файла.
2. Если по хэшу файл удалось найти в локальном хранилище, файл возвращается пользователю.

## Авторизация

Тип авторизации пользователей: **Basic**. Регистрация пользователей в сервисе не предусмотрена, два тестовых пользователя представлены в **Config**.

## API

### Upload
- **Endpoint**: /upload
- **Method**: POST
- **Headers**:
    - Authorization: Basic Auth
- **Body**: Файл в формате multipart/form-data
- **Response**: JSON объект с полем hash (хэш загруженного файла)

### Delete
- **Endpoint**: /delete/{file_hash}
- **Method**: POST
- **Headers**:
    - Authorization: Basic Auth
- **Query Params**: hash (хэш файла)
- **Response**: JSON объект с полем status (успех/неудача)

### Download
- **Endpoint**: /download/{file_hash}
- **Method**: GET
- **Query Params**: hash (хэш файла)
- **Response**: Файл, если найден в хранилище

## Установка и запуск

### Используя Docker:

1. Клонируйте репозиторий:
```bash
$ git clone https://github.com/webcachee/DrWeb-test.git 
```

2. Выполните команду:
```bash
$ make app
```

### Инструкция по запуску вручную:

1. Клонируйте репозиторий:
```bash
$ git clone https://github.com/webcachee/DrWeb-test.git 
```

2. Загрузите зависимости:
```bash
$ poetry install
```

3. Активируйте виртуальное окружение:
```bash
$ poetry shell
```

4. Запустите **entrypoint.sh** для запуска приложения:
```bash
$  source entrypoint.sh
```

### Реализованные make команды

- `make app` - запуск контейнера приложения
- `make app-logs` - просмотр логов в контейнере приложения
- `make app-down` - выключить контейнер с приложением
- `make run-test` - запуск тестов внутри приложения

## Тесты

Запуск тестов внутри **Docker**-контейнера:
```bash
$ make run-test
```

Тестируются все основные функции приложения:
- Загрузка файла **(/upload)**
- Скачивание файла **(/upload/{file_hash})**
- Удаление файла **(/delete/{file_hash})**

## .env

Пример **.env** файла представлен в **.env.example**:

```
USER1_PASSWORD=password1
USER2_PASSWORD=password2
DEBUG=False
```