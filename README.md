# TrelloLikeAPI — Асинхронный Backend на FastAPI

**REST API для управления задачами и командами**  
Команды, доски, задачи, пользователи, авторизация через JWT.
Система использует базу данных Postgresql.

---

## Особенности

- **FastAPI** — современный, быстрый, с автодокументацией  
- **Асинхронный SQLAlchemy 2.0+** с `asyncpg`  
- **JWT-авторизация** через `PyJWT`  
- **Защита роутов** через `Depends`  
- **Чистая архитектура**: `routers/`, `crud/`, `schemas/`, `models/`  
- **Docker + docker-compose** — запуск одной командой  
- **Swagger UI** — `/docs`, `/redoc`
- **.env** - задает параметры окружения (присутсвует .env.exmaple)

---

## Структура проекта

```
TrelloLikeAPI/
├── app
│   ├── crud             # CRUD operations
│   │   ├── auth
│   │   │   └── registration.py
│   │   ├── board
│   │   │   └── board_actions.py
│   │   ├── task
│   │   │   └── task_actions.py
│   │   └── team
│   │       └── team_actions.py
│   │
│   ├── database.py      # database information
│   ├── dependencies.py  # database session manger
│   ├── main.py
│   ├── routers          # routers
│   │   ├── auth.py
│   │   ├── board.py
│   │   ├── task.py
│   │   └── teams.py
│   │
│   ├── security        # JWT creation and validation
│   │   └── core.py
│   │
│   ├── settings.py     # extract .env params 
│   ├── shecemas        # Pydantic
│   │   ├── auth_shecema.py
│   │   ├── board_schema.py
│   │   ├── tasks_shema.py
│   │   └── teams_schema.py
│   │
│   └── table_models   # SqlAclhemy models
│       ├── base.py
│       ├── boards.py
│       ├── __init__.py
│       ├── tasks.py
│       ├── team.py
│       └── user.py
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── tests           # test
    ├── conftest.py
    ├── test_auth.py
    ├── test_boards.py
    ├── test_tasks.py
    └── test_teams.py
```
---

## Описание endpoits:
Ниже перечислены основные endpoint'ы API, их назначение, доступ и примеры запросов/ответов.  
Во всех примерах авторизация передаётся заголовком:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## /auth

### POST `/auth/register`
**Описание:** Регистрация нового пользователя.  
**Доступ:** Все (без авторизации)  
**Тело (JSON):**
```json
{
  "username": "alice",
  "password": "secure123",
  "surename": "Алисова"
}
```
**Успех:** `201 Created`  
**Пример ответа:**
```json
{
  "token": "ey... (JWT)"
}
```
**Ошибки:**
- `409 Conflict` — пользователь с таким именем уже существует  
- `422 Unprocessable Entity` — ошибка валидации

**Пример curl:**
```bash
curl -X POST "http://example.com/auth/register"   -H "Content-Type: application/json"   -d '{"username":"alice","password":"secure123","surename":"Алисова"}'
```

---

### POST `/auth/login`
**Описание:** Аутентификация, выдача JWT.  
**Доступ:** Все  
**Тело (JSON):**
```json
{
  "username": "alice",
  "password": "secure123"
}
```
**Успех:** `200 OK`  
**Пример ответа:**
```json
{ "token": "ey... (JWT)" }
```
**Ошибки:**
- `401 Unauthorized` — неверный логин/пароль

**Пример curl:**
```bash
curl -X POST "http://example.com/auth/login"   -H "Content-Type: application/json"   -d '{"username":"alice","password":"secure123"}'
```

---

## /teams

### POST `/teams/`
**Описание:** Создать команду.  
**Доступ:** Авторизованные пользователи (JWT)  
**Тело (JSON):**
```json
{
  "name": "team_alpha"
}
```
**Успех:** `201 Created`  
**Пример ответа:**
```json
{ "id": 123, "name": "team_alpha", "owner_id": 10 }
```

**Пример curl:**
```bash
curl -X POST "http://example.com/teams/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"name":"team_alpha"}'
```

---

### POST `/teams/{team_name}/invite`
**Описание:** Пригласить пользователя в команду по email.  
**Доступ:** Только владелец команды (Owner)  
**Тело (JSON):**
```json
{ "email": "invitee@example.com" }
```
**Успех:** `200 OK` или `201 Created` (в зависимости от реализации)  
**Ошибки:**
- `403/401` — недостаточно прав  
- `404` — команда не найдена

---

### PATCH `/teams/{team_name}/update_role`
**Описание:** Изменить роль члена команды
**Доступ:** Только владелец
**Успех:** `200 OK` — роль изменена успешно

---

### GET `/teams/{team_id}/boards`
**Описание:** Получить список досок команды.  
**Доступ:** Любой участник команды  
**Параметры:** (опционально) пагинация, фильтры по имени и т.п.  
**Успех:** `200 OK` — массив досок

---

## /boards

### POST `/boards/`
**Описание:** Создать доску в указанной команде.  
**Доступ:** Роль Manager и выше (Admin/Owner)  
**Тело (JSON):**
```json
{
  "name": "Board Name",
  "team_name": "team_alpha"
}
```
**Успех:** `201 Created`  
**Ошибки:**
- `401 Unauthorized` — нет токена/недостаточно прав  
- `404 Not Found` — команда не найдена  
- `409 Conflict` — доска с таким именем уже существует

**Пример curl:**
```bash
curl -X POST "http://example.com/boards/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"name":"HDDDD","team_name":"team_alpha"}'
```

---

### POST `/boards/{board_name}/tasks`
**Описание:** Получить информацию о всех заданяи доски
**Доступ:** Все участники команды 
**Успех:** `200 OK`  
**Ошибки:**
- `404 Not Found` — команда\доска\участник команды не найдена  

---

### DELETE `/delete`
**Описание:** Удалить доску
**Доступ:** Только владелец (Owner) 
**Успех:** `200 OK`  
**Ошибки:**
- `404 Not Found` — команда\доска команды не найдена  
- `409 CONFLICT` — неудалось удалить доску  

---

## /tasks

### POST `/tasks/`
**Описание:** Создать задачу на доске.  
**Доступ:** Участник команды  
**Тело (JSON):**
```json
{
  "status": "ToDo",
  "team": "team_alpha",
  "board": "Board Name",
  "title": "someOne",
  "description": "опционально"
}
```
**Успех:** `201 Created` 
**Ошибки:**
- `404 Not Found` — команда/доска не найдены  
- `401 UNAUTHORIZED` — недостаточно прав

**Пример curl:**
```bash
curl -X POST "http://example.com/tasks/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"status":"ToDo","team":"team_alpha","board":"Board Name","title":"someOne"}'
```

---

### PATCH `/tasks/new_status`
**Описание:** Переместить задачу в другую колонку/статус.  
**Доступ:** Участник команды 
**Тело (JSON):**
```json
{ "status": "ToDo" }
```
**Успех:** `200 OK` — обновлённая задача  
**Ошибки:**
- `409 CONFLICT` — задача/доска/участник команды не найдены  
---

### GET `/tasks/` (фильтры)
**Описание:** Получить список задач с фильтрами (пример: `priority` и `due_date`).  
**Пример запроса:**
```
GET /tasks/?priority=high&due_date=2025-11-01
```
**Доступ:** Участник команды  
**Успех:** `200 OK` — массив задач, соответствующих фильтрам

---

## Общие примечания и рекомендации
- Все ответы с ошибками возвращают JSON вида:
```json
{ "detail": "описание ошибки" }
```


## Быстрый старт

### С Docker (рекомендуется)

```bash
git clone https://github.com/yourname/TrelloLikeAPI.git
cd TrelloLikeAPI
docker-compose up --build