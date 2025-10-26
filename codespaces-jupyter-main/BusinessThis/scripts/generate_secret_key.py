#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for BusinessThis deployment
"""
import secrets
import string

def generate_secret_key():
    """Generate a secure random secret key"""
    # Generate a 32-character URL-safe random string
    secret_key = secrets.token_urlsafe(32)
    return secret_key

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("Generated SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    print("\nAdd this to your .env file and Vercel environment variables.")
