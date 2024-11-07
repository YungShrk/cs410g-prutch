# Filename: environment_script.py
import os

def get_secret_key():
    """
    Get secret key from environment variable.
    """
    return os.getenv("SECRET_KEY", "default_key")

print("Secret Key:", get_secret_key())

