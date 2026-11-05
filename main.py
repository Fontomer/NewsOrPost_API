# This is a simple API for news and their authors using FastAPI
# Это простой API для новостей и их авторов с использованием FastAPI
# author / автор: Ethereal Darkness (@cxber)
# language: en / ru

# Type one of the following commands in the URL to get the desired information:
# Введите одну из следующих команд в URL, чтобы получить нужную информацию:

# /news - get all news / получить все новости
# /contacts - get all authors / получить всех авторов
# /news/{id} - get news by id / получить новость по id
# /news/add - add news / добавить новость
# /contacts/add - add author / добавить автора
# /search?news_id=1 - search news by id / поиск новости по id



# _________________Import________________________

from fastapi import FastAPI, HTTPException, Query, Path, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from models import Base, User, News
from database import SessionLocal, engine
from schemas import UserCreate, NewsCreate, NewsRe, User as DbUser

#_________________DataBase_______________________

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#_________________Commands_______________________

@app.post('/users/', response_model=DbUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


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


@app.get('/news/', response_model=List[NewsRe])
def get_news(db: Session = Depends(get_db)) -> List[NewsRe]:
    return db.query(News).all()

@app.get('/contacts/', response_model=List[DbUser])
def get_users(db: Session = Depends(get_db)) -> List[DbUser]:
    return db.query(User).all()


@app.get('/')
def homepage() -> Dict[str, str]:
    return {'message': 'hi there! this is a simple API for news and their authors'} 
# # добавить текст в несколько строк и написать подссылки которые он поддерживает

#_________________Other__________________________

# @app.get('/news/{id}')
# async def items(id: Annotated[
#     int, Path(..., title='Type here a news ID for search', ge=1)
#     ]) -> News:
#     for news in allnews:
#         if news['id'] == id:
#             return News(**news)

#     raise HTTPException(status_code=404, detail=f'News with number {id} not found')


# @app.get('/search')
# async def search(news_id: Annotated[
#     Optional[int], 
#     Query(title='ID of news to search', ge=1)
# ]) -> Dict[str, Optional[News]]:
#     if news_id is not None:
#         for news in allnews:
#             if news['id'] == news_id:
#                 return {'data': News(**news)}
#         raise HTTPException(status_code=404, detail=f'News with number {news_id} not found')
#     return {'data': None}