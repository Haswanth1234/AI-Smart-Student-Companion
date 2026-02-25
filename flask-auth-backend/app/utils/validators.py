import re

def validate_email(email):
    """
    Validate email format
    Args: email (str)
    Returns: Boolean
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password (minimum 6 characters)
    Args: password (str)
    Returns: Boolean
    """
    return len(password) >= 6

def validate_phone(phone):
    """
    Validate phone number (10 digits, Indian format)
    Args: phone (str)
    Returns: Boolean
    """
    if not phone:
        return True  # Phone is optional
    
    # Remove spaces, dashes, and country code
    cleaned_phone = re.sub(r'[\s\-\+]', '', phone)
    
    # Check if it's 10 digits (Indian mobile)
    if re.match(r'^[6-9]\d{9}$', cleaned_phone):
        return True
    
    # Check if it has country code +91 followed by 10 digits
    if re.match(r'^91[6-9]\d{9}$', cleaned_phone):
        return True
    
    return False

def validate_required_fields(data, required_fields):
    """
    Check if all required fields are present
    Args:
        data (dict) - Request data
        required_fields (list) - List of required field names
    Returns: Tuple (is_valid: bool, missing_fields: list)
    """
    missing_fields = [field for field in required_fields if not data.get(field)]
    return len(missing_fields) == 0, missing_fields