from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Base User Schema
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.CUSTOMER
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        import re
        # Basic phone validation - accepts +, digits, spaces, hyphens
        if not re.match(r'^\+?[\d\s-]{10,}$', v):
            raise ValueError('Invalid phone number format')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = None
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return v
        import re
        if not re.match(r'^\+?[\d\s-]{10,}$', v):
            raise ValueError('Invalid phone number format')
        return v

class UserChangePassword(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('Passwords do not match')
        return v

class UserRoleUpdate(BaseModel):
    role: UserRole

class UserStatusUpdate(BaseModel):
    status: UserStatus

# User Response Schema
class User(UserBase):
    id: int
    status: UserStatus
    avatar: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserWithToken(User):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

# Refresh Token Schema
class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# User List Response
class UserListResponse(BaseModel):
    items: List[User]
    total: int
    page: int
    per_page: int
    total_pages: int