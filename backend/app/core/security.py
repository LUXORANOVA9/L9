"""
LUXORANOVA Security Utilities
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
import pyotp
import qrcode
from io import BytesIO
import base64

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================================
# Password Hashing
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# JWT Token Management
# ============================================================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_token_type(token: str, expected_type: str) -> bool:
    """
    Verify the type of a JWT token.
    
    Args:
        token: JWT token to verify
        expected_type: Expected token type ('access' or 'refresh')
        
    Returns:
        True if token type matches, False otherwise
    """
    payload = decode_token(token)
    if not payload:
        return False
    
    return payload.get("type") == expected_type


# ============================================================================
# API Key Management
# ============================================================================

def generate_api_key() -> tuple[str, str]:
    """
    Generate a new API key.
    
    Returns:
        Tuple of (full_key, prefix) where:
        - full_key: Complete API key to give to user
        - prefix: First 8 characters for identification
    """
    # Generate random key
    key = secrets.token_urlsafe(32)
    
    # Add prefix
    full_key = f"{settings.API_KEY_PREFIX}{key}"
    
    # Get prefix for storage (first 8 chars after prefix)
    prefix = full_key[:len(settings.API_KEY_PREFIX) + 8]
    
    return full_key, prefix


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for storage.
    
    Args:
        api_key: API key to hash
        
    Returns:
        Hashed API key
    """
    return hash_password(api_key)


def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    """
    Verify an API key against a hash.
    
    Args:
        plain_key: Plain text API key
        hashed_key: Hashed API key
        
    Returns:
        True if key matches, False otherwise
    """
    return verify_password(plain_key, hashed_key)


# ============================================================================
# Multi-Factor Authentication (MFA)
# ============================================================================

def generate_mfa_secret() -> str:
    """
    Generate a new MFA secret.
    
    Returns:
        Base32 encoded secret
    """
    return pyotp.random_base32()


def generate_mfa_qr_code(secret: str, email: str) -> str:
    """
    Generate a QR code for MFA setup.
    
    Args:
        secret: MFA secret
        email: User email
        
    Returns:
        Base64 encoded QR code image
    """
    # Create provisioning URI
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=email,
        issuer_name=settings.APP_NAME
    )
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def verify_mfa_code(secret: str, code: str) -> bool:
    """
    Verify an MFA code.
    
    Args:
        secret: MFA secret
        code: 6-digit code to verify
        
    Returns:
        True if code is valid, False otherwise
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


def generate_backup_codes(count: int = 10) -> list[str]:
    """
    Generate backup codes for MFA.
    
    Args:
        count: Number of backup codes to generate
        
    Returns:
        List of backup codes
    """
    return [secrets.token_hex(4).upper() for _ in range(count)]


# ============================================================================
# Password Reset Tokens
# ============================================================================

def create_password_reset_token(email: str) -> str:
    """
    Create a password reset token.
    
    Args:
        email: User email
        
    Returns:
        Password reset token
    """
    data = {
        "email": email,
        "type": "password_reset"
    }
    
    expire = datetime.utcnow() + timedelta(hours=1)
    data.update({"exp": expire})
    
    token = jwt.encode(
        data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token.
    
    Args:
        token: Password reset token
        
    Returns:
        Email if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        if payload.get("type") != "password_reset":
            return None
        
        return payload.get("email")
    except JWTError:
        return None


# ============================================================================
# Email Verification Tokens
# ============================================================================

def create_email_verification_token(email: str) -> str:
    """
    Create an email verification token.
    
    Args:
        email: User email
        
    Returns:
        Email verification token
    """
    data = {
        "email": email,
        "type": "email_verification"
    }
    
    expire = datetime.utcnow() + timedelta(days=7)
    data.update({"exp": expire})
    
    token = jwt.encode(
        data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def verify_email_verification_token(token: str) -> Optional[str]:
    """
    Verify an email verification token.
    
    Args:
        token: Email verification token
        
    Returns:
        Email if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        if payload.get("type") != "email_verification":
            return None
        
        return payload.get("email")
    except JWTError:
        return None


# ============================================================================
# Session Management
# ============================================================================

def generate_session_id() -> str:
    """
    Generate a unique session ID.
    
    Returns:
        Session ID
    """
    return secrets.token_urlsafe(32)


# ============================================================================
# CSRF Protection
# ============================================================================

def generate_csrf_token() -> str:
    """
    Generate a CSRF token.
    
    Returns:
        CSRF token
    """
    return secrets.token_urlsafe(32)


def verify_csrf_token(token: str, expected_token: str) -> bool:
    """
    Verify a CSRF token.
    
    Args:
        token: Token to verify
        expected_token: Expected token value
        
    Returns:
        True if tokens match, False otherwise
    """
    return secrets.compare_digest(token, expected_token)


# ============================================================================
# Encryption Utilities
# ============================================================================

def encrypt_data(data: str) -> str:
    """
    Encrypt sensitive data.
    
    Args:
        data: Data to encrypt
        
    Returns:
        Encrypted data
    """
    # TODO: Implement encryption using cryptography library
    # For now, return base64 encoded (NOT SECURE - placeholder)
    return base64.b64encode(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """
    Decrypt sensitive data.
    
    Args:
        encrypted_data: Encrypted data
        
    Returns:
        Decrypted data
    """
    # TODO: Implement decryption using cryptography library
    # For now, return base64 decoded (NOT SECURE - placeholder)
    return base64.b64decode(encrypted_data.encode()).decode()


# ============================================================================
# Rate Limiting Helpers
# ============================================================================

def generate_rate_limit_key(identifier: str, endpoint: str) -> str:
    """
    Generate a rate limit key.
    
    Args:
        identifier: User identifier (IP, user ID, API key)
        endpoint: API endpoint
        
    Returns:
        Rate limit key
    """
    return f"ratelimit:{endpoint}:{identifier}"


# ============================================================================
# Security Headers
# ============================================================================

def get_security_headers() -> Dict[str, str]:
    """
    Get recommended security headers.
    
    Returns:
        Dictionary of security headers
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
    }
