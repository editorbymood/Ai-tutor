# AI Tutor Platform - Complete File Connectivity & Functionality Map

## 🎯 Executive Summary

This document provides a complete analysis of how all files in the AI Tutor platform connect and interact with each other. The project is a full-stack educational platform with Django REST API backend and React frontend, featuring AI-powered tutoring, course management, assessments, and analytics.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Pages   │  │Components│  │  Redux   │  │ Services │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │          │
│       └─────────────┴─────────────┴─────────────┘          │
│                           │                                 │
│                       API Calls                             │
└───────────────────────────┼─────────────────────────────────┘
                            │
                       HTTP/HTTPS
                            │
┌───────────────────────────┼─────────────────────────────────┐
│                      BACKEND (Django)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   URLs   │──│  Views   │──│Serializers│──│  Models  │   │
│  └──────────┘  └────┬─────┘  └──────────┘  └────┬─────┘   │
│                     │                           │          │
│            ┌────────┴────────┐          ┌───────┴───────┐  │
│            │                  │          │               │  │
│       ┌────▼───┐      ┌──────▼─────┐   │      ┌───────▼──┐│
│       │ Gemini │      │   Celery   │   │      │ Database ││
│       │   AI   │      │   Tasks    │   │      │ (MongoDB)││
│       └────────┘      └──────┬─────┘   │      └──────────┘│
│                             │          │                   │
│                       ┌─────▼──────┐   │                   │
│                       │    Redis   │───┘                   │
│                       │   Cache    │                       │
│                       └────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Detailed File Connectivity Map

### 1. Entry Points & Configuration

#### **manage.py** → Entry Point
```
manage.py
    ├── Sets DJANGO_SETTINGS_MODULE to 'backend.settings'
    ├── Calls django.setup()
    └── Executes management commands
```

#### **backend/config/settings.py** → Core Configuration
```
settings.py
    ├── Defines INSTALLED_APPS (all Django apps)
    ├── Configures DATABASES (MongoDB via djongo / SQLite for tests)
    ├── Sets up REST_FRAMEWORK settings
    ├── Configures JWT authentication
    ├── Sets up CACHES (Redis / LocMem)
    ├── Configures CELERY settings
    └── Imports from: python-decouple for environment variables
```

#### **backend/urls.py** → URL Routing Hub
```
backend/urls.py
    ├── Includes apps.users.urls → /api/auth/*
    ├── Includes apps.courses.urls → /api/courses/*
    ├── Includes apps.assessments.urls → /api/assessments/*
    ├── Includes apps.ai_tutor.urls → /api/ai-tutor/*
    ├── Includes apps.analytics.urls → /api/analytics/*
    ├── Includes apps.gamification.urls → /api/gamification/*
    ├── Includes apps.social.urls → /api/social/*
    ├── Includes apps.voice.urls → /api/voice/*
    ├── Maps health check endpoints → backend/health.py
    └── Admin site → django.contrib.admin
```

#### **backend/__init__.py** → Celery Initialization
```
backend/__init__.py
    └── Imports celery app from backend.celery
```

#### **backend/celery.py** → Async Task Queue
```
backend/celery.py
    ├── Creates Celery app instance
    ├── Loads config from Django settings
    ├── Autodiscovers tasks from all apps
    └── Used by: apps/ai_tutor/tasks.py
```

---

### 2. User Management Flow (apps/users/)

#### **apps/users/models.py**
```
User Model (Custom AbstractUser)
    ├── Fields: email, role, learning_style, etc.
    ├── Used by: All other apps (ForeignKey relationships)
    ├── Relationships:
    │   ├── OneToOne: UserPreferences
    │   ├── OneToOne: LearningAnalytics
    │   └── ManyToMany: Course (through Enrollment)

LearningStyleAssessment Model
    ├── ForeignKey: User
    └── Stores VARK assessment scores

UserPreferences Model
    ├── OneToOne: User
    └── Stores UI and learning preferences
```

#### **apps/users/views.py**
```
Authentication Views
    ├── register_user()
    │   ├── Uses: UserRegistrationSerializer
    │   ├── Creates: User, UserPreferences
    │   ├── Returns: JWT tokens
    │   └── Calls: RefreshToken.for_user()
    │
    ├── login_user()
    │   ├── Uses: authenticate()
    │   ├── Returns: JWT tokens
    │   └── Calls: UserProfileSerializer
    │
    ├── logout_user()
    │   └── Blacklists refresh token
    │
    ├── get_current_user()
    │   └── Returns: UserProfileSerializer
    │
    ├── update_profile()
    │   └── Updates: User model
    │
    └── change_password()
        └── Updates: User.set_password()

Class-Based Views
    ├── LearningStyleAssessmentView
    │   └── Creates: LearningStyleAssessment
    │
    └── UserPreferencesView
        └── Updates: UserPreferences
```

#### **apps/users/serializers.py**
```
UserRegistrationSerializer
    ├── Validates: password, email
    ├── Creates: User via UserManager
    └── Used by: register_user()

UserProfileSerializer
    ├── Read-only user data
    └── Used by: login, get_current_user

LearningStyleAssessmentSerializer
    ├── Determines style from scores
    └── Updates: User.learning_style

UserPreferencesSerializer
    └── Manages: theme, language, AI settings
```

#### **apps/users/urls.py**
```
URL Patterns
    ├── /register/ → register_user
    ├── /login/ → login_user
    ├── /logout/ → logout_user
    ├── /profile/ → get_current_user
    ├── /profile/update/ → update_profile
    ├── /password/change/ → change_password
    ├── /assessment/ → LearningStyleAssessmentView
    └── /preferences/ → UserPreferencesView
```

---

### 3. Course Management Flow (apps/courses/)

#### **apps/courses/models.py**
```
Course Model
    ├── ForeignKey: User (instructor)
    ├── ManyToMany: User (students, through Enrollment)
    ├── Related: Lesson, Quiz, Enrollment
    └── Properties: total_lessons, total_students

Lesson Model
    ├── ForeignKey: Course
    └── Fields: content, video_url, order

Enrollment Model
    ├── ForeignKey: User (student)
    ├── ForeignKey: Course
    └── Related: LessonProgress

LessonProgress Model
    ├── ForeignKey: Enrollment
    ├── ForeignKey: Lesson
    └── Tracks: completion, time_spent

CourseReview Model
    ├── ForeignKey: Course
    ├── ForeignKey: User (student)
    └── Fields: rating, sentiment_score
```

#### **apps/courses/views.py**
```
CourseListCreateView
    ├── GET: Lists published courses
    │   ├── Filters: category, difficulty, search
    │   └── Returns: CourseListSerializer
    └── POST: Creates course (teachers only)
        └── Uses: CourseSerializer

CourseDetailView
    ├── GET: Course details
    └── PUT/DELETE: Update/delete (instructor only)

enroll_course()
    ├── Creates: Enrollment
    └── Checks: duplicate enrollment

my_enrollments()
    └── Lists: User's enrollments

update_lesson_progress()
    ├── Creates/Updates: LessonProgress
    ├── Updates: Enrollment.completed_lessons
    └── Calls: enrollment.update_progress()

CourseReviewListCreateView
    ├── Lists: Course reviews
    └── Creates: Review (enrolled students only)
```

#### **apps/courses/permissions.py**
```
IsTeacherOrReadOnly
    └── Allows: Teachers to create/edit, all to read

IsEnrolledStudent
    └── Checks: Enrollment exists
```

---

### 4. Assessment Flow (apps/assessments/)

#### **apps/assessments/models.py**
```
Quiz Model
    ├── ForeignKey: Course, User (created_by)
    └── Related: Question, QuizAttempt

Question Model
    ├── ForeignKey: Quiz
    └── Related: Answer

Answer Model
    ├── ForeignKey: Question
    └── Field: is_correct

QuizAttempt Model
    ├── ForeignKey: Quiz, User (student)
    ├── Related: QuestionResponse
    └── Method: calculate_score()

QuestionResponse Model
    ├── ForeignKey: QuizAttempt, Question
    └── ForeignKey: Answer (selected_answer)
```

#### **apps/assessments/views.py**
```
QuizListView
    └── Lists: Published quizzes for course

start_quiz_attempt()
    ├── Checks: max_attempts limit
    └── Creates: QuizAttempt

submit_answer()
    ├── Creates/Updates: QuestionResponse
    └── Calculates: is_correct, points_earned

complete_quiz_attempt()
    ├── Calls: attempt.calculate_score()
    └── Updates: status, completed_at, time_taken

my_quiz_attempts()
    └── Lists: User's quiz attempts
```

---

### 5. AI Tutor Flow (apps/ai_tutor/)

#### **apps/ai_tutor/models.py**
```
ChatSession Model
    ├── ForeignKey: User, Course (optional), Lesson (optional)
    └── Related: ChatMessage

ChatMessage Model
    ├── ForeignKey: ChatSession
    └── Fields: role, content, model_used

AIGeneratedContent Model
    ├── ForeignKey: User (created_by), Course, Lesson
    └── Fields: prompt, generated_content

StudyRecommendation Model
    ├── ForeignKey: User, Course, Lesson
    └── Fields: title, reason, priority
```

#### **apps/ai_tutor/views.py**
```
ChatSessionListCreateView
    └── Creates/Lists: ChatSession

send_chat_message()
    ├── Creates: ChatMessage (user)
    ├── Calls: gemini_service.chat()
    ├── Creates: ChatMessage (AI response)
    └── Uses: User.learning_style for context

generate_lesson_content()
    ├── Calls: gemini_service.generate_lesson()
    └── Creates: AIGeneratedContent

generate_quiz()
    ├── Calls: gemini_service.generate_quiz()
    └── Creates: AIGeneratedContent

explain_concept()
    └── Calls: gemini_service.explain_concept()
```

#### **apps/ai_tutor/gemini_service.py**
```
GeminiService Class
    ├── __init__(): Creates Gemini model
    ├── generate_content(): Basic content generation
    ├── chat(): Conversational AI
    ├── generate_lesson(): Lesson generation (cached)
    ├── generate_quiz(): Quiz generation (cached)
    ├── explain_concept(): Concept explanation (cached)
    └── provide_feedback(): Answer feedback

cache_ai_response() Decorator
    ├── Uses: Redis cache
    └── Caches: Successful AI responses
```

#### **apps/ai_tutor/tasks.py**
```
Celery Tasks (Async)
    └── generate_content_async()
        └── Runs: AI content generation in background
```

---

### 6. Analytics Flow (apps/analytics/)

#### **apps/analytics/models.py**
```
UserActivity Model
    ├── ForeignKey: User
    └── Tracks: activity_type, metadata

LearningAnalytics Model
    ├── OneToOne: User
    └── Fields: study_time, streaks, scores

CourseAnalytics Model
    ├── OneToOne: Course
    └── Fields: enrollment_count, completion_rate
```

#### **apps/analytics/views.py**
```
get_student_dashboard()
    ├── Gets: LearningAnalytics
    ├── Queries: Enrollment, QuizAttempt
    └── Returns: Comprehensive dashboard data

get_teacher_dashboard()
    ├── Queries: Courses taught
    ├── Aggregates: Enrollment stats
    └── Returns: Course performance metrics

get_course_analytics()
    ├── Gets: CourseAnalytics
    ├── Calculates: Progress distribution
    └── Returns: Detailed course metrics

log_activity()
    └── Creates: UserActivity
```

---

### 7. ML Models (apps/ml_models/)

#### **apps/ml_models/learning_style_detector.py**
```
LearningStyleDetector Class
    ├── Uses: K-means clustering
    ├── extract_features(): User interaction data
    ├── train(): Trains model on data
    ├── predict(): Predicts learning style
    ├── save_model(): Saves to ML_MODELS_DIR
    └── load_model(): Loads trained model
```

#### **apps/ml_models/performance_predictor.py**
```
PerformancePredictor Class
    ├── Uses: Random Forest classifier
    ├── extract_features(): Student metrics
    ├── train(): Trains model
    ├── predict(): Predicts at-risk/on-track/excelling
    └── get_feature_importance(): Feature analysis
```

#### **apps/ml_models/sentiment_analyzer.py**
```
SentimentAnalyzer Class
    ├── Uses: TextBlob
    └── analyze(): Returns sentiment score
```

---

### 8. Frontend (React)

#### **frontend/src/App.js**
```
App Component
    ├── Uses: React Router
    ├── Routes:
    │   ├── /login → Login
    │   ├── /register → Register
    │   ├── /dashboard → StudentDashboard / TeacherDashboard
    │   ├── /courses → Courses
    │   ├── /courses/:id → CourseDetail
    │   ├── /quiz/:id → Quiz
    │   ├── /ai-tutor → AITutor
    │   └── /profile → Profile
    └── Uses: PrivateRoute for auth protection
```

#### **frontend/src/redux/store.js**
```
Redux Store
    ├── Slices:
    │   ├── authSlice: User authentication state
    │   ├── coursesSlice: Course data
    │   └── aiTutorSlice: AI chat state
    └── Middleware: Redux Toolkit defaults
```

#### **frontend/src/services/api.js**
```
API Service
    ├── Axios instance with baseURL
    ├── Interceptors for JWT tokens
    └── API methods:
        ├── auth.login()
        ├── courses.list()
        ├── assessments.startQuiz()
        └── aiTutor.sendMessage()
```

---

## 🔄 Data Flow Examples

### Example 1: Student Takes a Quiz

```
1. Frontend: Student clicks "Start Quiz"
   └── Quiz.js → dispatch(startQuizAttempt(quizId))
   
2. Redux: aiTutorSlice updates
   └── api.post('/api/assessments/quizzes/{id}/start/')
   
3. Backend: Route matching
   └── backend/urls.py → apps.assessments.urls
   
4. View: start_quiz_attempt()
   ├── Checks max_attempts
   ├── Creates QuizAttempt
   └── Returns QuizAttemptSerializer
   
5. Database: QuizAttempt saved
   └── MongoDB/SQLite
   
6. Frontend: Receives attempt data
   └── Quiz.js displays questions
   
7. Frontend: Student submits answers
   └── api.post('/api/assessments/attempts/{id}/answer/')
   
8. Backend: submit_answer()
   ├── Creates QuestionResponse
   └── Validates answer
   
9. Frontend: Complete quiz
   └── api.post('/api/assessments/attempts/{id}/complete/')
   
10. Backend: complete_quiz_attempt()
    ├── Calls attempt.calculate_score()
    ├── Updates status
    └── Returns score data
    
11. Frontend: Shows results
    └── Quiz.js displays score and feedback
```

### Example 2: AI Content Generation

```
1. Frontend: Teacher requests lesson generation
   └── AITutor.js → dispatch(generateLesson({topic, difficulty}))
   
2. API Call
   └── api.post('/api/ai-tutor/generate/lesson/', data)
   
3. Backend: generate_lesson_content()
   ├── Gets user's learning_style
   └── Calls gemini_service.generate_lesson()
   
4. Gemini Service: cache_ai_response decorator
   ├── Checks Redis cache
   └── If miss, calls Gemini API
   
5. Google Gemini API
   └── Returns generated lesson content
   
6. Cache: Store response
   └── Redis.set(key, content, timeout=7200)
   
7. Database: Save AIGeneratedContent
   └── MongoDB/SQLite
   
8. Response: Return to frontend
   └── AIGeneratedContentSerializer
   
9. Frontend: Display lesson
   └── AITutor.js shows generated content
```

---

## 🔧 Utility & Helper Files

### **backend/utils.py**
```
custom_exception_handler()
    └── Standardizes DRF errors

success_response()
    └── Consistent success format

error_response()
    └── Consistent error format
```

### **backend/health.py**
```
health_check()
    └── Basic health endpoint

readiness_check()
    ├── Checks database
    ├── Checks Redis
    └── Checks cache

metrics()
    └── System metrics (CPU, memory)
```

---

## 📦 Dependencies & Integrations

### Python Packages (requirements.txt)
```
Django 4.2.7
    └── Core framework

djangorestframework 3.14.0
    └── API framework

djangorestframework-simplejwt 5.3.0
    └── JWT authentication

djongo 1.3.6
    └── MongoDB integration

celery 5.3.4
    └── Async task queue

redis 5.0.1
    └── Caching layer

google-generativeai 0.3.1
    └── Gemini AI API

scikit-learn 1.3.2
    └── ML models

pytest 7.4.3
    └── Testing framework
```

### NPM Packages (frontend/package.json)
```
react 18.2.0
    └── UI framework

@reduxjs/toolkit 1.9.7
    └── State management

@mui/material 5.14.19
    └── UI components

axios 1.6.2
    └── HTTP client

react-router-dom 6.20.1
    └── Routing
```

---

## 🧪 Testing Infrastructure

### Test Files Connectivity

```
tests/conftest.py
    ├── Defines fixtures: api_client, student_user, teacher_user
    └── Used by: All test files

tests/test_complete_integration.py
    ├── Uses: conftest fixtures
    ├── Tests: Full user journeys
    └── Classes:
        ├── TestCompleteUserJourney
        ├── TestCourseManagement
        ├── TestAssessments
        ├── TestAITutor
        ├── TestAnalytics
        ├── TestPermissions
        ├── TestDataValidation
        └── TestEdgeCases

run_all_tests.py
    ├── Runs: All test suites
    ├── Checks: Database, Redis, Config
    └── Generates: Coverage reports
```

---

## 🔒 Security Flow

### Authentication Chain
```
1. User Login
   └── apps/users/views.py:login_user()
   
2. JWT Generation
   └── simplejwt.tokens.RefreshToken.for_user()
   
3. Token Storage
   └── Frontend: localStorage / Redux state
   
4. API Request
   └── Axios interceptor adds: Authorization: Bearer {token}
   
5. Backend Validation
   └── JWTAuthentication.authenticate()
   
6. Permission Check
   └── IsAuthenticated, IsTeacherOrReadOnly, etc.
   
7. View Execution
   └── If authorized, proceed
```

---

## 📈 Performance Optimizations

### Caching Strategy
```
Redis Cache
    ├── AI Responses (2 hours)
    │   └── gemini_service: Lesson, quiz, explanations
    │
    ├── User Sessions (default)
    │   └── Django session backend
    │
    └── Celery Results (default)
        └── Task execution results
```

### Database Optimization
```
MongoDB/SQLite
    ├── Indexes: email, role, learning_style
    ├── Connection Pooling: maxPoolSize=100
    └── Query Optimization: select_related, prefetch_related
```

---

## 🎯 Critical File Dependencies

### Must-Have Files for System to Function

1. **Configuration**
   - `backend/settings.py` - Core config
   - `backend/urls.py` - URL routing
   - `backend/celery.py` - Async tasks
   - `.env` - Environment variables

2. **Core Models**
   - `apps/users/models.py` - User authentication
   - `apps/courses/models.py` - Course data
   - `apps/assessments/models.py` - Quizzes
   - `apps/ai_tutor/models.py` - AI interactions

3. **Views & Serializers**
   - All `views.py` files - API endpoints
   - All `serializers.py` files - Data validation

4. **Frontend**
   - `frontend/src/App.js` - Main component
   - `frontend/src/redux/store.js` - State management
   - `frontend/src/services/api.js` - API communication

---

## ✅ Verification Checklist

To verify all connections are working:

- [ ] Database connection (MongoDB/SQLite)
- [ ] Redis connection
- [ ] Gemini API key configured
- [ ] All apps in INSTALLED_APPS
- [ ] All URL patterns registered
- [ ] Celery worker running
- [ ] Frontend can reach backend API
- [ ] JWT authentication working
- [ ] File uploads configured
- [ ] Static files serving
- [ ] Tests passing

---

**Last Updated**: 2025-10-22
**Total Files Analyzed**: 100+
**Connectivity Status**: ✅ Fully Mapped
