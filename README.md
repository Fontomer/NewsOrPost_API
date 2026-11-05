# NewsOrPost_API
Небольшой проект по проектированию реляционной базы данных новостного сайта и связка их с помощью **SQLite** и **FastAPI** через **Python**.

## 🎯 Цель проекта
- Спроектировать модель данных для базовой социальной системы;
- Написать и протестировать **SQLAlchemy** для создания таблиц и внешних ключей;
- Выполнить запросы для базы данных, а так же на практике понять как что работает;

## 🛠 Технологии
- **Database:** SQLite
- **API:** FastAPI x Python
- **Key Concepts:** `@app.(get/post)`, `SessionLocal`, `Annotated`, `relationship`, `ForeignKey`

–––––

## 📐 Структура базы данных

База состоит из двух основных таблиц:

1. **`users`** — профили авторов (`id`, `name`, `age`).
2. **`news`** — статьи написанные авторами (`id`, `title`, `body`, `author_id`).

–––––

## 🔍 Основные URL запросы

### 1. Показ всех новостей 
Запрос показывает все новости из базы данных новостей:

```python
@app.get('/news/', response_model=List[NewsRe])
def get_news(db: Session = Depends(get_db)) -> List[NewsRe]:
    return db.query(News).all()
```
_Пример запроса_
```http
http://127.0.0.1:8000/news/
```

### 2. Показ всех авторов статей
Запрос показывает всех авторов статей:

```python
@app.get('/contacts/', response_model=List[DbUser])
def get_users(db: Session = Depends(get_db)) -> List[DbUser]:
    return db.query(User).all()
```

_Пример запроса_
```http
http://127.0.0.1:8000/contacts/
```

### 3. Поиск новости по его ID
Т.к. у каждой новости есть ID, то поиск выдаст только ту новость где ID поиска и новости совпадет:

```python
WIP
```

_Пример запроса_
```http
http://127.0.0.1:8000/news/1
```

### 4. Добавление новости и автора (*'/news/add'*) и (*'/contacts/add'*)
При создании новости/автора информация добавляется в базу данных и сохраняется в файле `test.db`:

Для новости:

```python
@app.post('/news/', response_model=NewsRe)
def create_news(news: NewsCreate, db: Session = Depends(get_db)) -> NewsRe:
    db_user = db.query(User).filter(User.id == news.author_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f'Author with ID {news.author_id} not found')

    db_news = News(title=news.title, body=news.body, author_id=news.author_id)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    return db_news
```

Для автора:
```python
@app.post('/users/', response_model=DbUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
```

–––––

## 🚀 Как запустить проект локально
1. Установите любой pythonIDE.
2. Установите модули SQLAlchemy, FastAPI(Standart), если не установились автоматически
3. Создайте свою базу данных или возьмите мою.
4. Выполните скрипт из файла `main.py` введя в терминал `fastapi dev main.py`
5. Перейти на созданный в терминале локальный сайт (по умолчанию это `http://127.0.0.1:8000/`)
