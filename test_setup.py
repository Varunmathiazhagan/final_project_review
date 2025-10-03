#!/usr/bin/env python3
"""
Quick validation test for the SQLi scanner setup.
Run this to verify all dependencies are installed correctly.
"""
import sys

def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    errors = []
    
    try:
        import streamlit
        print("✅ streamlit")
    except ImportError as e:
        errors.append(f"❌ streamlit: {e}")
    
    try:
        import aiohttp
        print("✅ aiohttp")
    except ImportError as e:
        errors.append(f"❌ aiohttp: {e}")
    
    try:
        import bs4
        print("✅ beautifulsoup4")
    except ImportError as e:
        errors.append(f"❌ beautifulsoup4: {e}")
    
    try:
        import lxml
        print("✅ lxml")
    except ImportError as e:
        errors.append(f"⚠️  lxml (optional): {e}")
    
    try:
        import reportlab
        print("✅ reportlab")
    except ImportError as e:
        errors.append(f"⚠️  reportlab (optional): {e}")
    
    try:
        from playwright.async_api import async_playwright
        print("✅ playwright")
    except ImportError as e:
        errors.append(f"⚠️  playwright (optional): {e}")
    
    try:
        import flask
        print("✅ flask")
    except ImportError as e:
        errors.append(f"❌ flask: {e}")
    
    return errors

def test_scanner_import():
    """Test that the scanner can be imported."""
    print("\nTesting scanner import...")
    try:
        from app import AsyncSQLiScanner
        print("✅ AsyncSQLiScanner imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import AsyncSQLiScanner: {e}")
        return False

def main():
    print("=" * 60)
    print("SQLi Scanner Setup Validation")
    print("=" * 60)
    
    errors = test_imports()
    scanner_ok = test_scanner_import()
    
    print("\n" + "=" * 60)
    if errors:
        print("⚠️  Some dependencies had issues:")
        for err in errors:
            if err.startswith("❌"):
                print(err)
    
    if not scanner_ok:
        print("❌ Scanner import failed")
        sys.exit(1)
    
    print("\n✅ Setup validation complete!")
    print("\nNext steps:")
    print("  • For Streamlit UI: streamlit run streamlit_app.py")
    print("  • For Flask UI: python dashboard.py")
    print("  • For CLI: python app.py --start-url http://testphp.vulnweb.com")
    print("\n⚠️  Remember: Only scan authorized targets!")

if __name__ == "__main__":
    main()
