import re

def is_valid_email(email):
    """Check if the given string is a valid email address."""
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email) is not None

def is_valid_password(password):
    """Check if the given string meets password requirements."""
    return len(password) >= 6  

def sanitize_input(input_string):
    """Sanitize the input string to prevent potential security vulnerabilities."""
    return re.sub('<[^<]+?>', '', input_string)
