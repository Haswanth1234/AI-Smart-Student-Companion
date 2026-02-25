import bcrypt

def hash_password(password):
    """
    Hash password using bcrypt
    Args: password (str) - Plain text password
    Returns: Hashed password string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verify password against hash
    Args: 
        password (str) - Plain text password
        hashed_password (str) - Hashed password from database
    Returns: Boolean - True if password matches
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))