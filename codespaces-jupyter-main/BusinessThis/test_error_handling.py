#!/usr/bin/env python3
"""
Test error handling functionality
"""
from core.utils.error_handler import ValidationError, AuthenticationError

try:
    raise ValidationError("Test validation error")
except ValidationError as e:
    print(f"Error handling works: {e.status_code == 400}")
    print(f"Error code: {e.error_code}")
    print(f"Message: {e.message}")
