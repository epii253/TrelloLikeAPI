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
**Успешный ответ:**
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
**Успешный ответ:**
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
**Примичание:** Создатель автоматически становится владельцем команды. 

**Тело (JSON):**
```json
{
  "name": "team_alpha"
}
```
**Успех:** `201 Created`  
**Успешный ответ:**
```json
{"detail": "Team created", "name": "team_name" }
```

**Пример curl:**
```bash
curl -X POST "http://example.com/teams/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"name":"team_alpha"}'
```

---

### POST `/teams/{team_name}/invite`
**Описание:** Пригласить пользователя в команду по UserName.  
**Доступ:** Только владелец команды (Owner)  
**Тело (JSON):**
```json
{ "username": "alice" }
```
**Успех:** `201 Created`  
**Успешный ответ**
```json
{"detail": "user added"}
```

**Ошибки:**
- `409` - Не найдена либо команда, либо не найдет пользователь с заданным UserName. Либо же пользователь уже находится в команде.
- `401` — недостаточно прав  

---

### PATCH `/teams/{team_name}/update_role`
**Описание:** Изменить роль члена команды. 
**Доступ:** Только владелец. 

**Успех:** `200 OK` — роль изменена успешно. 
**Успешный ответ**
```json
{"detail": "role updated", "new_role": "target_role"}
```

**Пример curl:**
```bash
curl -X POST "http://example.com/teams/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"username":"alice", "role": "admin"}'
```

**Ошибки:**
- `409` - Не найдена либо команда, либо не найдет пользователь с заданным UserName.
- `401` — недостаточно прав

---

### GET `/teams/{team_id}/boards`
**Описание:** Получить список досок команды.  
**Доступ:** Любой участник команды  
**Успешный ответ**
```json
{ "boards": ["name1", ...] }
```
**Успех:** `200 OK` — массив досок команды.

---

## /boards

### POST `/boards/`
**Описание:** Создать доску в указанной команде.  
**Доступ:** Роль Admin и Owner  
**Тело (JSON):**
```json
{
  "name": "Board Name",
  "team_name": "team_alpha"
}
```

**Успех:** `201 Created`  
**Успешный ответ**
```json
{"detail": "Board created"}
```

**Ошибки:**
- `401 Unauthorized` — нет токена/недостаточно прав  
- `404 Not Found` — команда не найдена  
- `409 Conflict` — доска с таким именем уже существует или неуспешное создание

**Пример curl:**
```bash
curl -X POST "http://example.com/boards/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"name":"Targets","team_name":"ICPC_Absolute_Team"}'
```

---

### POST `/boards/{board_name}/tasks
**Описание:** Получить информацию о всех заданяи доски
**Доступ:** Все участники команды 

**Успех:** `200 OK`  
**Успешный ответ**
```json
{
  "details": [{"task_tittle": {"status": "ToDo", "description": "Hmm"}}, ...]
}
```
**Ошибки:**
- `404 Not Found` — команда\доска\участник команды не найдена  

---

### DELETE `/delete?name="board_name"&team_name="super_team"`
**Описание:** Удалить доску
**Доступ:** Владелец (owner) и админ (admin) 
**Успех:** `200 OK`  
**Успешный ответ**
```json
{"detail": "Board deleted"}
```


**Ошибки:**
- `401 UNAUTHORIZED` - недостаточно прав
- `404 Not Found` — команда\доска команды не найдена  
- `409 CONFLICT` — неудалось удалить доску  

---

## /tasks

### POST `/tasks/`
**Описание:** Создать задачу на доске.  
**Доступ:** Владелец (owner) и админ (admin)  
**Тело (JSON):**
```json
{
  "status": "ToDo",
  "team": "team_alpha",
  "board": "Board Name",
  "title": "ICPC_Winners",
  "description": "mayBeNull"
}
```
**Успех:** `201 Created` 
**Успешный ответ**
```json
{"detail": "task created", "task_status": "target_status"}
```

**Ошибки:**
- `401 UNAUTHORIZED` — недостаточно прав
- `409 CONFLICT` — команда/доска/член команды не найдены

**Пример curl:**
```bash
curl -X POST "http://example.com/tasks/"   -H "Authorization: Bearer <TOKEN>"   -H "Content-Type: application/json"   -d '{"status":"ToDo","team":"team_alpha","board":"Board Name","title":"ICPC_Winners"}'
```

---

### PATCH `/tasks/new_status`
**Описание:** Обновить статус задачи на доске.  
**Доступ:** Участник команды 
**Тело (JSON):**
```json
{ 
  "team": "labmdaTeam",
  "board": "BlackMesa",
  "tittle": "CrystalExperiment",
  "new_status": "ToDo" 
}
```
**Успех:** `200 OK` — обновлённая задача  
**Успешный ответ**
```json
{"detail": "status updated", "new_status": "target_status"}
```

**Ошибки:**
- `409 CONFLICT` — задача/доска/участник команды не найдены 
---


## Быстрый старт

### С Docker (рекомендуется)

```bash
git clone https://github.com/yourname/TrelloLikeAPI.git
cd TrelloLikeAPI
touch .env
cat .env.examle > .env
docker-compose up --build