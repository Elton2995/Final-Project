from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class SystemSettingBase(BaseModel):
    setting_key: str = Field(..., max_length=100)
    setting_value: str
    description: Optional[str] = Field(None, max_length=500)
    is_public: bool = False

class SystemSettingCreate(SystemSettingBase):
    pass

class SystemSettingUpdate(BaseModel):
    setting_value: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    is_public: Optional[bool] = None

class SystemSetting(SystemSettingBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SystemSettingListResponse(BaseModel):
    items: List[SystemSetting]
    total: int

class SystemSettingsUpdate(BaseModel):
    settings: Dict[str, str]