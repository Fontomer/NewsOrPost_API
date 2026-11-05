from pydantic import BaseModel, Field
from typing import Annotated


#User classes
class UserBase(BaseModel):
    name: Annotated[str, Field(..., title='Type name', min_length=2, max_length=20)]
    age: Annotated[int, Field(..., title='Type age (1-80 y.o)', ge=1, le=80)]

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }


#News classes
class NewsBase(BaseModel):
    title: Annotated[str, Field(..., title='Type a news title', min_length=1, max_length=100)]
    body: Annotated[str, Field(..., title='Type a news body', min_length=1, max_length=1000)]
    author_id: int

class NewsCreate(NewsBase):
    pass

class NewsRe(NewsBase):
    id: int
    author: User

    model_config = {
        "from_attributes": True
    }