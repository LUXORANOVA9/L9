"""
LUXORANOVA User Schemas
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from app.models.user import UserRole, UserStatus


# ============================================================================
# User Authentication Schemas
# ============================================================================

class UserLogin(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    mfa_code: Optional[str] = Field(None, min_length=6, max_length=6)


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """JWT token payload data."""
    user_id: str
    email: str
    role: UserRole
    tenant_id: Optional[str] = None


# ============================================================================
# User CRUD Schemas
# ============================================================================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=128)
    tenant_id: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    preferences: Optional[dict] = None


class UserPasswordUpdate(BaseModel):
    """Schema for updating user password."""
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    status: UserStatus
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    tenant_id: Optional[str] = None
    subscription_plan: Optional[str] = None
    subscription_status: Optional[str] = None
    api_key: Optional[str] = None
    mfa_enabled: bool
    email_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""
    users: List[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# MFA Schemas
# ============================================================================

class MFASetupRequest(BaseModel):
    """Schema for MFA setup request."""
    password: str = Field(..., min_length=8)


class MFASetupResponse(BaseModel):
    """Schema for MFA setup response."""
    secret: str
    qr_code_url: str
    backup_codes: List[str]


class MFAVerifyRequest(BaseModel):
    """Schema for MFA verification request."""
    code: str = Field(..., min_length=6, max_length=6)


class MFADisableRequest(BaseModel):
    """Schema for MFA disable request."""
    password: str = Field(..., min_length=8)
    code: str = Field(..., min_length=6, max_length=6)


# ============================================================================
# API Key Schemas
# ============================================================================

class APIKeyCreate(BaseModel):
    """Schema for creating API key."""
    name: str = Field(..., min_length=1, max_length=255)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


class APIKeyResponse(BaseModel):
    """Schema for API key response."""
    id: str
    name: str
    key: str
    prefix: str
    expires_at: Optional[datetime] = None
    created_at: datetime
    last_used_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class APIKeyListResponse(BaseModel):
    """Schema for API key list response."""
    keys: List[APIKeyResponse]
    total: int


# ============================================================================
# Subscription Schemas
# ============================================================================

class SubscriptionUpdate(BaseModel):
    """Schema for updating subscription."""
    plan: str = Field(..., pattern="^(free|professional|enterprise)$")
    billing_cycle: str = Field(..., pattern="^(monthly|yearly)$")


class SubscriptionResponse(BaseModel):
    """Schema for subscription response."""
    plan: str
    status: str
    billing_cycle: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool
    monthly_tasks_limit: int
    monthly_tasks_used: int
    agents_limit: int
    
    class Config:
        from_attributes = True


# ============================================================================
# User Preferences Schemas
# ============================================================================

class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences."""
    theme: Optional[str] = Field(None, pattern="^(light|dark|auto)$")
    language: Optional[str] = Field(None, pattern="^[a-z]{2}$")
    timezone: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    email_notifications: Optional[bool] = None
    default_model: Optional[str] = None
    custom_settings: Optional[dict] = None


# ============================================================================
# Password Reset Schemas
# ============================================================================

class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    
    @validator('new_password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


# ============================================================================
# Email Verification Schemas
# ============================================================================

class EmailVerificationRequest(BaseModel):
    """Schema for email verification request."""
    email: EmailStr


class EmailVerificationConfirm(BaseModel):
    """Schema for email verification confirmation."""
    token: str
