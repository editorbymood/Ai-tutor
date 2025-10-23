#!/usr/bin/env python3
"""
Comprehensive project file checker - identifies missing and required files.
"""
import os
from pathlib import Path
import json

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def check_frontend_files():
    """Check frontend files and identify missing ones."""
    print_header("Frontend Files Check")
    
    frontend_dir = Path("frontend")
    missing_files = []
    
    # Critical frontend files
    required_files = {
        "public": [
            "index.html",
            "manifest.json",
            "favicon.ico",
            "logo192.png",
            "logo512.png",
            "robots.txt"
        ],
        "src": [
            "index.js",
            "index.css",
            "App.js",
            "App.css",
            "reportWebVitals.js"
        ],
        "src/components": [
            "Layout.js",
            "PrivateRoute.js",
            "Loading.js",
            "ErrorBoundary.js"
        ],
        "src/pages": [
            "Login.js",
            "Register.js",
            "StudentDashboard.js",
            "TeacherDashboard.js",
            "Courses.js",
            "CourseDetail.js",
            "AITutor.js",
            "Quiz.js",
            "Profile.js"
        ],
        "src/redux/slices": [
            "authSlice.js",
            "coursesSlice.js",
            "aiTutorSlice.js"
        ],
        "src/services": [
            "api.js"
        ],
        ".": [
            "package.json",
            ".env.example",
            ".gitignore"
        ]
    }
    
    for directory, files in required_files.items():
        dir_path = frontend_dir / directory if directory != "." else frontend_dir
        print(f"📁 Checking {dir_path}...")
        
        for file in files:
            file_path = dir_path / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✅ {file} ({size} bytes)")
            else:
                print(f"  ❌ {file} - MISSING")
                missing_files.append(str(file_path))
    
    return missing_files

def check_backend_files():
    """Check backend files."""
    print_header("Backend Files Check")
    
    missing_files = []
    
    # Django apps to check
    apps = [
        "users", "courses", "assessments", "ai_tutor",
        "analytics", "ml_models", "gamification", "social", "voice"
    ]
    
    required_app_files = [
        "__init__.py",
        "apps.py",
        "models.py",
        "views.py",
        "serializers.py",
        "urls.py",
        "admin.py"
    ]
    
    for app in apps:
        app_dir = Path(f"apps/{app}")
        print(f"📁 Checking app: {app}...")
        
        if not app_dir.exists():
            print(f"  ❌ App directory missing!")
            continue
        
        for file in required_app_files:
            file_path = app_dir / file
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✅ {file} ({size} bytes)")
            else:
                print(f"  ❌ {file} - MISSING")
                missing_files.append(str(file_path))
    
    # Backend config files
    print(f"\n📁 Checking backend config...")
    backend_files = [
        "backend/__init__.py",
        "backend/celery.py",
        "backend/settings.py",
        "backend/urls.py",
        "backend/wsgi.py",
        "backend/utils.py",
        "backend/health.py",
        "backend/config/settings.py",
        "backend/config/urls.py",
        "backend/config/wsgi.py",
        "backend/config/asgi.py"
    ]
    
    for file_path_str in backend_files:
        file_path = Path(file_path_str)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file_path.name} ({size} bytes)")
        else:
            print(f"  ❌ {file_path_str} - MISSING")
    
    return missing_files

def check_css_and_assets():
    """Check for CSS and asset files."""
    print_header("CSS & Assets Check")
    
    css_dirs = [
        "frontend/src",
        "frontend/src/components",
        "frontend/src/pages",
        "frontend/public"
    ]
    
    missing_css = []
    
    for dir_path_str in css_dirs:
        dir_path = Path(dir_path_str)
        if dir_path.exists():
            css_files = list(dir_path.glob("*.css"))
            scss_files = list(dir_path.glob("*.scss"))
            
            if css_files or scss_files:
                print(f"📁 {dir_path}:")
                for file in css_files + scss_files:
                    print(f"  ✅ {file.name} ({file.stat().st_size} bytes)")
            else:
                print(f"📁 {dir_path}: ⚠️  No CSS files found")
    
    # Check for images
    print(f"\n📁 Checking public assets...")
    public_dir = Path("frontend/public")
    if public_dir.exists():
        images = list(public_dir.glob("*.png")) + list(public_dir.glob("*.jpg")) + \
                list(public_dir.glob("*.ico")) + list(public_dir.glob("*.svg"))
        
        if images:
            for img in images:
                print(f"  ✅ {img.name}")
        else:
            print(f"  ⚠️  No images found - may need favicon.ico, logos")
            missing_css.append("frontend/public/favicon.ico")
            missing_css.append("frontend/public/logo192.png")
            missing_css.append("frontend/public/logo512.png")
    
    return missing_css

def check_config_files():
    """Check configuration files."""
    print_header("Configuration Files Check")
    
    config_files = [
        ".env.example",
        ".gitignore",
        "docker-compose.yml",
        "docker-compose.production.yml",
        "requirements.txt",
        "pytest.ini",
        "setup.py",
        "README.md"
    ]
    
    missing = []
    for file_name in config_files:
        file_path = Path(file_name)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file_name} ({size:,} bytes)")
        else:
            print(f"  ❌ {file_name} - MISSING")
            missing.append(file_name)
    
    return missing

def main():
    """Main check function."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "COMPREHENSIVE PROJECT FILE CHECK" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    
    os.chdir(Path(__file__).parent)
    
    all_missing = []
    
    # Run all checks
    all_missing.extend(check_frontend_files())
    all_missing.extend(check_backend_files())
    all_missing.extend(check_css_and_assets())
    all_missing.extend(check_config_files())
    
    # Summary
    print_header("Summary")
    
    if all_missing:
        print(f"❌ Found {len(all_missing)} missing files:\n")
        for file in all_missing:
            print(f"  - {file}")
        
        print(f"\n💡 Recommendation: Create these missing files")
    else:
        print("✅ All critical files present!")
    
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()
