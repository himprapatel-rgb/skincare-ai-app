"""Pydantic schemas for user notifications."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    """Schema for creating a notification."""
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., max_length=1000)
    notification_type: str  # reminder, analysis_result, routine_tip, achievement
    related_id: Optional[int] = None
    priority: str = Field(default="normal", description="Priority: low, normal, high")


class NotificationPreferences(BaseModel):
    """User notification preferences."""
    email_notifications: bool = True
    push_notifications: bool = True
    routine_reminders: bool = True
    analysis_updates: bool = True
    tips_and_recommendations: bool = True
    marketing_emails: bool = False


class NotificationResponse(BaseModel):
    """Notification response schema."""
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    related_id: Optional[int]
    priority: str
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Paginated list of notifications."""
    total: int
    unread_count: int
    page: int
    page_size: int
    items: List[NotificationResponse]


class NotificationBulkUpdate(BaseModel):
    """Bulk update notifications (mark as read)."""
    notification_ids: List[int]
    is_read: bool