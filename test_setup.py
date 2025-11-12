#!/usr/bin/env python3
"""
Quick test script to verify the application setup
Run this before starting the app to check dependencies
"""

import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import flask
        print(f"✓ Flask {flask.__version__}")
    except ImportError as e:
        print(f"✗ Flask not found: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print(f"✓ Flask-SQLAlchemy")
    except ImportError as e:
        print(f"✗ Flask-SQLAlchemy not found: {e}")
        return False
    
    try:
        import PIL
        print(f"✓ Pillow {PIL.__version__}")
    except ImportError as e:
        print(f"✗ Pillow not found: {e}")
        return False
    
    try:
        import reportlab
        print(f"✓ ReportLab")
    except ImportError as e:
        print(f"✗ ReportLab not found: {e}")
        return False
    
    try:
        import dotenv
        print(f"✓ python-dotenv")
    except ImportError as e:
        print(f"✗ python-dotenv not found: {e}")
        return False
    
    return True

def test_app_syntax():
    """Test that app.py has no syntax errors"""
    print("\nTesting app.py syntax...")
    
    try:
        import app
        print("✓ app.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in app.py: {e}")
        return False
    except Exception as e:
        print(f"⚠ Warning: {e}")
        print("  (This may be normal if database is not configured)")
        return True

def test_templates():
    """Test that all required templates exist"""
    print("\nTesting templates...")
    import os
    
    templates = [
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/report.html'
    ]
    
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✓ {template}")
        else:
            print(f"✗ {template} not found")
            all_exist = False
    
    return all_exist

def test_config_files():
    """Test that configuration files exist"""
    print("\nTesting configuration files...")
    import os
    
    files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        '.env.example',
        '.gitignore'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} not found")
            all_exist = False
    
    # Check if .env exists (optional but recommended)
    if os.path.exists('.env'):
        print("✓ .env (configured)")
    else:
        print("⚠ .env not found (copy from .env.example)")
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 50)
    print("Ranger Signature Manager - Setup Test")
    print("=" * 50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("App Syntax", test_app_syntax()))
    results.append(("Templates", test_templates()))
    results.append(("Config Files", test_config_files()))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n✓ All tests passed! Ready to run the application.")
        print("\nStart the app with:")
        print("  ./run.sh")
        print("  or")
        print("  python app.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
