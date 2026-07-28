from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Full name of the candidate"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User password"
    )
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str    