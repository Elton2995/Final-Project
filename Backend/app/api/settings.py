from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional, List
import logging

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import require_admin
from app.schemas.settings import (
    SystemSetting,
    SystemSettingCreate,
    SystemSettingUpdate,
    SystemSettingListResponse,
    SystemSettingsUpdate
)
from app.schemas.common import ResponseMessage
from app.crud.audit_log import audit_log_crud
from app.models.system_settings import SystemSetting

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/settings",
    response_model=SystemSettingListResponse,
    summary="Get all settings",
    description="Get all system settings. Admin only."
)
async def get_settings(
    include_private: bool = False,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get all system settings."""
    query = db.query(SystemSetting)
    
    if not include_private:
        query = query.filter(SystemSetting.is_public == True)
    
    settings = query.all()
    
    return SystemSettingListResponse(
        items=settings,
        total=len(settings)
    )

@router.get(
    "/settings/public",
    response_model=dict,
    summary="Get public settings",
    description="Get public settings (no authentication required)."
)
async def get_public_settings(
    db: Session = Depends(get_db)
):
    """Get public system settings."""
    settings = db.query(SystemSetting).filter(
        SystemSetting.is_public == True
    ).all()
    
    return {
        setting.setting_key: setting.setting_value
        for setting in settings
    }

@router.get(
    "/settings/{setting_key}",
    response_model=SystemSetting,
    summary="Get setting by key",
    description="Get a specific setting. Admin only."
)
async def get_setting(
    setting_key: str,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get a specific setting."""
    setting = db.query(SystemSetting).filter(
        SystemSetting.setting_key == setting_key
    ).first()
    
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    return setting

@router.post(
    "/settings",
    response_model=SystemSetting,
    status_code=status.HTTP_201_CREATED,
    summary="Create setting",
    description="Create a new system setting. Admin only."
)
async def create_setting(
    setting_data: SystemSettingCreate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new system setting."""
    existing = db.query(SystemSetting).filter(
        SystemSetting.setting_key == setting_data.setting_key
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Setting key already exists"
        )
    
    setting = SystemSetting(**setting_data.model_dump())
    db.add(setting)
    db.commit()
    db.refresh(setting)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="create",
        resource_type="system_setting",
        resource_id=setting.id,
        details={"setting_key": setting.setting_key},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} created setting: {setting.setting_key}")
    
    return setting

@router.put(
    "/settings/{setting_key}",
    response_model=SystemSetting,
    summary="Update setting",
    description="Update a system setting. Admin only."
)
async def update_setting(
    setting_key: str,
    setting_data: SystemSettingUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update a system setting."""
    setting = db.query(SystemSetting).filter(
        SystemSetting.setting_key == setting_key
    ).first()
    
    if not setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setting not found"
        )
    
    for key, value in setting_data.model_dump(exclude_unset=True).items():
        setattr(setting, key, value)
    
    db.commit()
    db.refresh(setting)
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="update",
        resource_type="system_setting",
        resource_id=setting.id,
        details={"setting_key": setting.setting_key},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} updated setting: {setting.setting_key}")
    
    return setting

@router.post(
    "/settings/bulk",
    response_model=ResponseMessage,
    summary="Bulk update settings",
    description="Update multiple settings at once. Admin only."
)
async def bulk_update_settings(
    settings_data: SystemSettingsUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update multiple settings at once."""
    for key, value in settings_data.settings.items():
        setting = db.query(SystemSetting).filter(
            SystemSetting.setting_key == key
        ).first()
        
        if setting:
            setting.setting_value = value
        else:
            setting = SystemSetting(
                setting_key=key,
                setting_value=value,
                is_public=False
            )
            db.add(setting)
    
    db.commit()
    
    audit_log_crud.log_action(
        db,
        user_id=current_user.id,
        action="update",
        resource_type="system_setting",
        details={"updated_settings": list(settings_data.settings.keys())},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    logger.info(f"User {current_user.email} bulk updated {len(settings_data.settings)} settings")
    
    return ResponseMessage(
        message=f"Updated {len(settings_data.settings)} settings",
        success=True
    )