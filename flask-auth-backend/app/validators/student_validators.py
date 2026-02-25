def validate_studying_year(year):
    """
    Validate studying year (1-5)
    Args: year (int)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(year, int):
        return False, "Studying year must be an integer"
    
    if year < 1 or year > 5:
        return False, "Studying year must be between 1 and 5"
    
    return True, None


def validate_semester(semester):
    """
    Validate semester (1-10)
    Args: semester (int)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(semester, int):
        return False, "Semester must be an integer"
    
    if semester < 1 or semester > 10:
        return False, "Semester must be between 1 and 10"
    
    return True, None


def validate_semester_marks(marks):
    """
    Validate semester marks array
    Each mark should be 0-100
    Args: marks (list)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(marks, list):
        return False, "Semester marks must be an array"
    
    if len(marks) == 0:
        return False, "Semester marks cannot be empty"
    
    for item in marks:
        if not isinstance(item, dict):
            return False, "Each item must be a dictionary {subject, marks}"
        
        if 'subject' not in item or 'marks' not in item:
            return False, "Each item must have 'subject' and 'marks' keys"
            
        if not isinstance(item['marks'], (int, float)):
             return False, "Marks must be a number"
             
        if item['marks'] < 0 or item['marks'] > 100:
            return False, "Marks must be between 0 and 100"
            
        if not isinstance(item['subject'], str) or not item['subject'].strip():
            return False, "Subject must be a non-empty string"
            
    return True, None


def validate_attendance_percentage(percentage):
    """
    Validate attendance percentage (0-100)
    Args: percentage (float)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(percentage, (int, float)):
        return False, "Attendance percentage must be a number"
    
    if percentage < 0 or percentage > 100:
        return False, "Attendance percentage must be between 0 and 100"
    
    return True, None


def validate_interested_domain(domain):
    """
    Validate interested domain string
    Args: domain (str)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(domain, str):
        return False, "Interested domain must be a string"
    
    if len(domain.strip()) == 0:
        return False, "Interested domain cannot be empty"
    
    if len(domain) > 100:
        return False, "Interested domain must be less than 100 characters"
    
    return True, None


def validate_skills(skills):
    """
    Validate skills array
    Args: skills (list)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(skills, list):
        return False, "Skills must be an array"
    
    if len(skills) == 0:
        return False, "Skills cannot be empty"
    
    for skill in skills:
        if not isinstance(skill, str):
            return False, "Each skill must be a string"
        
        if len(skill.strip()) == 0:
            return False, "Skill cannot be empty"
    
    return True, None


def validate_passout_year(year):
    """
    Validate passout year (reasonable range)
    Args: year (int)
    Returns: tuple (is_valid: bool, error_message: str)
    """
    if not isinstance(year, int):
        return False, "Passout year must be an integer"
    
    from datetime import datetime
    current_year = datetime.now().year
    
    if year < current_year or year > current_year + 10:
        return False, f"Passout year must be between {current_year} and {current_year + 10}"
    
    return True, None


def validate_profile_data(data):
    """
    Validate entire profile update data
    Args: data (dict) - Profile fields to update
    Returns: tuple (is_valid: bool, errors: dict)
    """
    errors = {}
    
    # Validate each field if provided
    if 'studying_year' in data:
        is_valid, error_msg = validate_studying_year(data['studying_year'])
        if not is_valid:
            errors['studying_year'] = error_msg
    
    if 'semester' in data:
        is_valid, error_msg = validate_semester(data['semester'])
        if not is_valid:
            errors['semester'] = error_msg
    
    if 'semester_marks' in data:
        is_valid, error_msg = validate_semester_marks(data['semester_marks'])
        if not is_valid:
            errors['semester_marks'] = error_msg
    
    if 'attendance_percentage' in data:
        is_valid, error_msg = validate_attendance_percentage(data['attendance_percentage'])
        if not is_valid:
            errors['attendance_percentage'] = error_msg
    
    if 'interested_domain' in data:
        is_valid, error_msg = validate_interested_domain(data['interested_domain'])
        if not is_valid:
            errors['interested_domain'] = error_msg
    
    if 'skills' in data:
        is_valid, error_msg = validate_skills(data['skills'])
        if not is_valid:
            errors['skills'] = error_msg
    
    if 'passout_year' in data:
        is_valid, error_msg = validate_passout_year(data['passout_year'])
        if not is_valid:
            errors['passout_year'] = error_msg
    
    return len(errors) == 0, errors