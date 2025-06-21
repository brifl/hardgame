# utils.py
import secrets

# drop ambiguous characters: 0,1,o,l,i
ALPHABET = "23456789abcdefghjkmnpqrstuvwxyz"

def generate_code(length=6):
    """Return a short, unambiguous string code."""
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))
