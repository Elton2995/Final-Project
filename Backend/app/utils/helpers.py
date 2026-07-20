import random
import string
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json

def generate_random_string(length: int = 32) -> str:
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_verification_code(length: int = 6) -> str:
    """Generate a numeric verification code."""
    return ''.join(random.choices(string.digits, k=length))

def generate_reference_id(prefix: str, num: int, padding: int = 3) -> str:
    """Generate a reference ID like CMP-001, REQ-002."""
    return f"{prefix}-{str(num).zfill(padding)}"

def hash_data(data: str, secret: str) -> str:
    """Hash data using HMAC-SHA256."""
    return hmac.new(
        secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

def is_valid_uuid(uuid_str: str) -> bool:
    """Check if a string is a valid UUID."""
    import uuid
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def mask_email(email: str) -> str:
    """Mask email for privacy."""
    if '@' not in email:
        return email
    
    local, domain = email.split('@')
    if len(local) <= 2:
        masked_local = local[0] + '*' * (len(local) - 1)
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
    
    domain_parts = domain.split('.')
    if len(domain_parts[0]) <= 2:
        masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1)
    else:
        masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 2) + domain_parts[0][-1]
    
    return f"{masked_local}@{masked_domain}.{domain_parts[-1]}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def serialize_json(data: Dict[str, Any]) -> str:
    """Serialize dictionary to JSON string."""
    return json.dumps(data, default=str)

def deserialize_json(json_str: str) -> Dict[str, Any]:
    """Deserialize JSON string to dictionary."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}

def calculate_percentage(part: int, total: int) -> float:
    """Calculate percentage."""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)

def is_within_last_days(date: datetime, days: int) -> bool:
    """Check if a date is within the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    return date >= cutoff

def get_time_ago(date: datetime) -> str:
    """Get human-readable time ago string."""
    now = datetime.now()
    diff = now - date
    
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"