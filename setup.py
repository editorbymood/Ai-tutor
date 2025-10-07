"""
Setup script for AI-Powered Personal Tutor
"""
import os
import sys
import subprocess
import secrets


def generate_secret_key():
    """Generate a random secret key."""
    return secrets.token_urlsafe(50)


def create_env_file():
    """Create .env file from .env.example."""
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return
    
    if not os.path.exists('.env.example'):
        print("✗ .env.example not found")
        return
    
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Replace placeholders
    content = content.replace('your-secret-key-here-change-in-production', generate_secret_key())
    content = content.replace('your-jwt-secret-key-here', generate_secret_key())
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✓ Created .env file")
    print("⚠ Please update .env with your Gemini API key and other settings")


def install_backend_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing backend dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✓ Backend dependencies installed")
    except subprocess.CalledProcessError:
        print("✗ Failed to install backend dependencies")
        return False
    return True


def install_frontend_dependencies():
    """Install Node.js dependencies."""
    print("\n📦 Installing frontend dependencies...")
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'install'], check=True, shell=True)
        os.chdir('..')
        print("✓ Frontend dependencies installed")
    except subprocess.CalledProcessError:
        print("✗ Failed to install frontend dependencies")
        return False
    return True


def run_migrations():
    """Run Django migrations."""
    print("\n🔄 Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✓ Migrations completed")
    except subprocess.CalledProcessError:
        print("✗ Failed to run migrations")
        return False
    return True


def create_superuser():
    """Prompt to create superuser."""
    print("\n👤 Create superuser account")
    response = input("Do you want to create a superuser now? (y/n): ")
    if response.lower() == 'y':
        try:
            subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
            print("✓ Superuser created")
        except subprocess.CalledProcessError:
            print("✗ Failed to create superuser")


def main():
    """Main setup function."""
    print("=" * 60)
    print("AI-Powered Personal Tutor - Setup")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_backend_dependencies():
        print("\n❌ Setup failed at backend dependencies")
        return
    
    if not install_frontend_dependencies():
        print("\n❌ Setup failed at frontend dependencies")
        return
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Setup failed at migrations")
        return
    
    # Create superuser
    create_superuser()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update .env file with your Gemini API key")
    print("2. Start MongoDB: mongod")
    print("3. Start Redis: redis-server")
    print("4. Start backend: python manage.py runserver")
    print("5. Start frontend: cd frontend && npm start")
    print("6. Start Celery: celery -A backend worker -l info")
    print("\nOr use Docker:")
    print("docker-compose up -d")
    print("=" * 60)


if __name__ == '__main__':
    main()