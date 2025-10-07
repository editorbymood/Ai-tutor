# AI-Powered Personal Tutor (EdTech Platform)

A comprehensive AI-powered learning platform that personalizes education using Machine Learning and Large Language Models.

## 🚀 Features

### For Students
- **Personalized Learning**: AI analyzes your learning style and adapts content accordingly
- **AI Tutor Chat**: Real-time conversation with AI for explanations and help
- **Custom Quizzes**: Auto-generated quizzes based on your performance
- **Progress Analytics**: Visual dashboards showing your learning journey
- **Adaptive Content**: Lessons that adjust to your pace and understanding

### For Teachers
- **Student Analytics**: Comprehensive insights into student performance
- **Content Management**: Create and manage courses, lessons, and assessments
- **AI-Assisted Content**: Generate lesson plans and quizzes with AI
- **Class Management**: Monitor multiple students and classes
- **Performance Reports**: Detailed reports on student progress

### AI & ML Features
- **Learning Style Detection**: K-means clustering to identify learning patterns
- **Performance Prediction**: ML models predict student outcomes
- **Sentiment Analysis**: Analyze student feedback and engagement
- **Content Generation**: Gemini AI generates personalized lessons and explanations
- **Adaptive Difficulty**: Automatically adjusts content difficulty

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: MongoDB (via djongo)
- **AI/ML**: Google Gemini API, scikit-learn, NLTK
- **Authentication**: JWT (Simple JWT)
- **Task Queue**: Celery + Redis
- **Testing**: pytest

### Frontend
- **Framework**: React 18
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI (MUI)
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Routing**: React Router v6

### ML Models
- **Clustering**: K-means for learning style detection
- **Classification**: Random Forest for performance prediction
- **NLP**: TextBlob for sentiment analysis
- **LLM**: Google Gemini for content generation

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB 6.0+
- Redis 7.0+
- Google Gemini API Key

## 🔧 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd "ai powered tutor"
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json

# Start development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
copy .env.example .env.local
# Edit .env.local with your configuration

# Start development server
npm start
```

### 4. Start Redis (for Celery)

```bash
# Windows (if Redis is installed)
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

### 5. Start Celery Worker

```bash
# In a new terminal, activate venv and run:
celery -A backend worker -l info
```

## 🚀 Usage

1. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin

2. **Create accounts**:
   - Register as a student or teacher
   - Or use the admin panel to create users

3. **For Students**:
   - Complete the learning style assessment
   - Browse available courses
   - Chat with AI tutor
   - Take quizzes and track progress

4. **For Teachers**:
   - Create courses and lessons
   - Use AI to generate content
   - Monitor student progress
   - Generate reports

## 📁 Project Structure

```
ai-powered-tutor/
├── backend/                    # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/                 # User management & authentication
│   ├── courses/               # Course & lesson management
│   ├── assessments/           # Quizzes & tests
│   ├── ai_tutor/              # AI chat & content generation
│   ├── analytics/             # Progress tracking & analytics
│   └── ml_models/             # ML model training & inference
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── redux/            # State management
│   │   ├── services/         # API services
│   │   └── utils/            # Utility functions
│   └── public/
├── ml_models/                # Trained ML models
├── tests/                    # Test files
├── requirements.txt
└── README.md
```

## 🧪 Testing

### Backend Tests
```bash
pytest
pytest --cov=apps  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🔒 Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- CORS protection
- SQL injection prevention (via ORM)
- XSS protection
- CSRF protection
- Rate limiting on API endpoints
- Secure password hashing

## 📊 ML Models

### Learning Style Clustering
- Uses K-means to identify 4 learning styles: Visual, Auditory, Reading/Writing, Kinesthetic
- Features: interaction patterns, content preferences, performance metrics

### Performance Prediction
- Random Forest classifier predicts student success
- Features: quiz scores, time spent, engagement metrics, learning style

### Sentiment Analysis
- Analyzes student feedback and chat messages
- Helps identify struggling students early

## 🤖 AI Integration

### Google Gemini API
- Generates personalized lesson content
- Creates custom quizzes and questions
- Provides explanations in student's learning style
- Powers the AI tutor chat interface

## 🚢 Deployment

### Using Docker
```bash
docker-compose up -d
```

### Manual Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📝 API Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Your Name

## 🙏 Acknowledgments

- Google Gemini API for AI capabilities
- scikit-learn for ML models
- Django & React communities

## 📧 Support

For support, email support@aitutor.com or open an issue in the repository.