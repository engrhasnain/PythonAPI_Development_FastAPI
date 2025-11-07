from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime as DateTime
from typing import Optional

class Post(BaseModel):
    id: Optional[int] = None 
    title: str
    content: str
    published: bool = True
