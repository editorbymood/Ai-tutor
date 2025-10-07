# 🚀 Quick Start Guide

Get your AI-Powered Personal Tutor up and running in minutes!

## ⚡ Fastest Way to Start

### Option 1: Using Docker (Recommended - 5 minutes)

```bash
# 1. Get your Gemini API key from https://makersuite.google.com/app/apikey

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your GEMINI_API_KEY
notepad .env  # Windows
nano .env     # Linux/Mac

# 4. Start everything with Docker
docker-compose up -d

# 5. Create admin user
docker-compose exec backend python manage.py createsuperuser

# 6. Open your browser
# Frontend: http://localhost:3000
# Admin: http://localhost:8000/admin
```

### Option 2: Automated Setup (10 minutes)

**Windows:**
```bash
# 1. Install prerequisites:
# - Python 3.10+
# - Node.js 18+
# - MongoDB
# - Redis

# 2. Run setup
python setup.py

# 3. Add your GEMINI_API_KEY to .env

# 4. Start all services
start.bat
```

**Linux/Mac:**
```bash
# 1. Install prerequisites
# 2. Run setup
python setup.py

# 3. Add your GEMINI_API_KEY to .env

# 4. Make start script executable and run
chmod +x start.sh
./start.sh
```

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.10 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] MongoDB 6.0 or higher (or Docker)
- [ ] Redis 7.0 or higher (or Docker)
- [ ] Google Gemini API key (free at https://makersuite.google.com/app/apikey)

## 🎯 First Steps After Installation

### 1. Create Your Account

Visit http://localhost:3000 and:
- Click "Sign Up"
- Choose "Student" or "Teacher"
- Fill in your details
- Complete registration

### 2. For Students

**Complete Learning Style Assessment:**
1. Go to Profile
2. Take the learning style assessment
3. Get personalized recommendations

**Explore Courses:**
1. Browse available courses
2. Enroll in a course
3. Start learning!

**Try AI Tutor:**
1. Click "AI Tutor" in menu
2. Start a conversation
3. Ask questions about any topic

### 3. For Teachers

**Create Your First Course:**
1. Go to Dashboard
2. Click "Create Course"
3. Add course details
4. Add lessons

**Use AI to Generate Content:**
1. Use AI Tutor to generate lesson plans
2. Create quizzes automatically
3. Get content suggestions

**Monitor Students:**
1. View enrolled students
2. Track their progress
3. Identify students who need help

## 🔧 Configuration

### Essential Settings (.env file)

```env
# Required
GEMINI_API_KEY=your-api-key-here

# Optional (defaults work for development)
DEBUG=True
SECRET_KEY=auto-generated
MONGODB_HOST=localhost
REDIS_URL=redis://localhost:6379/0
```

### Frontend Settings (frontend/.env.local)

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🎓 Sample Data

Want to test with sample data?

```bash
# Create sample courses and users
python manage.py loaddata sample_data.json
```

Sample accounts:
- Student: student@example.com / password123
- Teacher: teacher@example.com / password123
- Admin: admin@example.com / password123

## 🐛 Common Issues & Solutions

### Issue: MongoDB Connection Error

**Solution:**
```bash
# Check if MongoDB is running
mongosh

# If not, start it
mongod

# Or use Docker
docker run -d -p 27017:27017 mongo:6.0
```

### Issue: Redis Connection Error

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# If not, start it
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

### Issue: Port Already in Use

**Solution:**
```bash
# Backend (port 8000)
python manage.py runserver 8001

# Frontend (port 3000)
PORT=3001 npm start
```

### Issue: Gemini API Error

**Solution:**
- Verify your API key in .env
- Check you have API quota remaining
- Ensure no extra spaces in the key

## 📚 Learning Resources

### Documentation
- [Full Setup Guide](SETUP_GUIDE.md) - Detailed installation
- [Project Overview](PROJECT_OVERVIEW.md) - Architecture & features
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [API Documentation](http://localhost:8000/api/docs/) - API reference

### Video Tutorials (Coming Soon)
- Installation walkthrough
- Creating your first course
- Using the AI Tutor
- Understanding analytics

## 🎯 What to Try First

### As a Student:
1. ✅ Complete learning style assessment
2. ✅ Enroll in a course
3. ✅ Chat with AI Tutor
4. ✅ Take a quiz
5. ✅ Check your progress dashboard

### As a Teacher:
1. ✅ Create a course
2. ✅ Use AI to generate a lesson
3. ✅ Create a quiz
4. ✅ View course analytics
5. ✅ Monitor student progress

## 🚀 Next Steps

Once you're comfortable with the basics:

1. **Customize the Platform**
   - Modify themes and colors
   - Add your branding
   - Customize email templates

2. **Integrate Additional Services**
   - Add payment gateway
   - Integrate video conferencing
   - Add social login

3. **Deploy to Production**
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)
   - Set up SSL/HTTPS
   - Configure backups

4. **Scale Your Platform**
   - Add more servers
   - Use CDN for static files
   - Optimize database queries

## 💡 Tips for Best Experience

1. **Use Chrome or Firefox** for best compatibility
2. **Enable notifications** to get real-time updates
3. **Complete your profile** for better personalization
4. **Take the learning style assessment** for optimal content
5. **Engage with AI Tutor** regularly for best results

## 🆘 Need Help?

- **Documentation:** Check the docs folder
- **Issues:** Open a GitHub issue
- **Email:** support@aitutor.com
- **Community:** Join our Discord/Slack

## 🎉 You're Ready!

Your AI-Powered Personal Tutor is now set up and ready to use!

**Access Points:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000/api
- 👨‍💼 Admin Panel: http://localhost:8000/admin
- 📚 API Docs: http://localhost:8000/api/docs/

**Happy Learning! 🎓🤖**

---

*For detailed information, see [SETUP_GUIDE.md](SETUP_GUIDE.md)*