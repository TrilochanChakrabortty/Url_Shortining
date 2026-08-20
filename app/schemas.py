from pydantic import BaseModel, HttpUrl, EmailStr, Field


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    click_count: int
    
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    
class UserLogin(BaseModel):
    username: str
    password: str