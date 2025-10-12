#!/usr/bin/env python3
"""
Script to fix logging issues in services
"""
import os
import re

def fix_logging_in_file(file_path):
    """Fix logging in a single file"""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if logging is already imported
    if 'import logging' not in content:
        # Add logging import after other imports
        lines = content.split('\n')
        import_line = -1
        for i, line in enumerate(lines):
            if line.startswith('from ') or line.startswith('import '):
                import_line = i
        
        if import_line >= 0:
            lines.insert(import_line + 1, 'import logging')
            content = '\n'.join(lines)
    
    # Replace print statements with logger
    content = re.sub(
        r'print\(f"Error ([^"]+)": \{e\}\)',
        r'logger = logging.getLogger(__name__)\n        logger.error(f"Error \1: {e}")',
        content
    )
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Fix logging in all service files"""
    service_files = [
        'services/auth_service.py',
        'services/financial_service.py', 
        'services/subscription_service.py',
        'services/ai_service.py',
        'services/admin_service.py',
        'services/reports_service.py',
        'services/email_service.py',
        'services/affiliate_service.py',
        'services/course_service.py',
        'services/multi_user_service.py',
        'services/advisor_service.py',
        'services/investment_service.py'
    ]
    
    fixed_count = 0
    for file_path in service_files:
        if fix_logging_in_file(file_path):
            print(f"✅ Fixed logging in {file_path}")
            fixed_count += 1
        else:
            print(f"⚠️  Could not fix {file_path}")
    
    print(f"\n📊 Fixed logging in {fixed_count}/{len(service_files)} files")

if __name__ == "__main__":
    main()
