import secrets

def generate_secure_5_digit_code():
    return f"{secrets.randbelow(100000):06d}"
