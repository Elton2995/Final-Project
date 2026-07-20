import re
from typing import Optional
from datetime import datetime

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove spaces, hyphens, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's a valid phone number (at least 10 digits)
    return bool(re.match(r'^\+?[0-9]{10,15}$', cleaned))

def validate_password(password: str) -> dict:
    """
    Validate password strength.
    Returns a dict with 'valid' and 'errors' keys.
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'[0-9]', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def validate_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

def validate_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """Validate date format."""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def sanitize_input(text: str) -> str:
    """Sanitize input text to prevent XSS."""
    if not text:
        return text
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove script tags
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL)
    
    # Escape special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#x27;')
    
    return text

def generate_slug(text: str) -> str:
    """Generate a URL-friendly slug from text."""
    # Convert to lowercase
    slug = text.lower()
    
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    
    # Replace spaces with hyphens
    slug = re.sub(r'[\s-]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug