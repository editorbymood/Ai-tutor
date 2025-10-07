"""
Load testing script for AI-Powered Personal Tutor.

This script simulates multiple concurrent users to test system performance.
Requires: pip install locust
"""
from locust import HttpUser, task, between, events
import random
import json
import logging

logger = logging.getLogger(__name__)


class StudentUser(HttpUser):
    """Simulates a student user behavior."""
    
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    def on_start(self):
        """Called when a user starts - login."""
        # Register a new user
        user_id = random.randint(1000, 999999)
        self.email = f"loadtest_student_{user_id}@test.com"
        self.password = "testpass123"
        
        # Try to register
        register_data = {
            "email": self.email,
            "password": self.password,
            "password2": self.password,
            "first_name": f"Student{user_id}",
            "last_name": "LoadTest",
            "role": "student"
        }
        
        response = self.client.post("/api/users/register/", json=register_data)
        
        # Login
        login_data = {
            "email": self.email,
            "password": self.password
        }
        
        response = self.client.post("/api/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('access')
            self.headers = {'Authorization': f'Bearer {self.token}'}
        else:
            logger.error(f"Login failed: {response.text}")
            self.headers = {}
    
    @task(3)
    def view_courses(self):
        """View course list."""
        self.client.get("/api/courses/", headers=self.headers)
    
    @task(2)
    def view_course_detail(self):
        """View a specific course."""
        # Assuming course IDs 1-10 exist
        course_id = random.randint(1, 10)
        self.client.get(f"/api/courses/{course_id}/", headers=self.headers)
    
    @task(1)
    def enroll_in_course(self):
        """Enroll in a course."""
        course_id = random.randint(1, 10)
        self.client.post(f"/api/courses/{course_id}/enroll/", headers=self.headers)
    
    @task(2)
    def view_profile(self):
        """View user profile."""
        self.client.get("/api/users/profile/", headers=self.headers)
    
    @task(1)
    def view_dashboard(self):
        """View student dashboard."""
        self.client.get("/api/analytics/student-dashboard/", headers=self.headers)
    
    @task(1)
    def chat_with_ai(self):
        """Send a message to AI tutor."""
        messages = [
            "What is Python?",
            "Explain variables",
            "How do I use loops?",
            "What are functions?",
            "Explain object-oriented programming"
        ]
        
        data = {
            "message": random.choice(messages)
        }
        
        self.client.post("/api/ai-tutor/chat/", json=data, headers=self.headers)


class TeacherUser(HttpUser):
    """Simulates a teacher user behavior."""
    
    wait_time = between(2, 8)  # Teachers typically take more time
    
    def on_start(self):
        """Called when a user starts - login."""
        user_id = random.randint(1000, 999999)
        self.email = f"loadtest_teacher_{user_id}@test.com"
        self.password = "testpass123"
        
        # Register
        register_data = {
            "email": self.email,
            "password": self.password,
            "password2": self.password,
            "first_name": f"Teacher{user_id}",
            "last_name": "LoadTest",
            "role": "teacher"
        }
        
        self.client.post("/api/users/register/", json=register_data)
        
        # Login
        login_data = {
            "email": self.email,
            "password": self.password
        }
        
        response = self.client.post("/api/users/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('access')
            self.headers = {'Authorization': f'Bearer {self.token}'}
        else:
            self.headers = {}
    
    @task(3)
    def view_my_courses(self):
        """View teacher's courses."""
        self.client.get("/api/courses/?instructor=me", headers=self.headers)
    
    @task(1)
    def create_course(self):
        """Create a new course."""
        course_id = random.randint(1000, 999999)
        data = {
            "title": f"Load Test Course {course_id}",
            "description": "This is a load test course",
            "difficulty": random.choice(["beginner", "intermediate", "advanced"]),
            "category": random.choice(["programming", "math", "science"]),
            "is_published": True
        }
        
        self.client.post("/api/courses/", json=data, headers=self.headers)
    
    @task(2)
    def view_teacher_dashboard(self):
        """View teacher dashboard."""
        self.client.get("/api/analytics/teacher-dashboard/", headers=self.headers)
    
    @task(1)
    def generate_lesson(self):
        """Generate lesson content with AI."""
        topics = ["Python Basics", "Data Structures", "Algorithms", "Web Development"]
        
        data = {
            "topic": random.choice(topics),
            "learning_style": random.choice(["visual", "auditory", "reading_writing", "kinesthetic"]),
            "difficulty": random.choice(["beginner", "intermediate", "advanced"])
        }
        
        self.client.post("/api/ai-tutor/generate-lesson/", json=data, headers=self.headers)


class AnonymousUser(HttpUser):
    """Simulates an anonymous user browsing."""
    
    wait_time = between(1, 3)
    
    @task(5)
    def view_public_courses(self):
        """View public course list."""
        self.client.get("/api/courses/")
    
    @task(2)
    def view_course_detail(self):
        """View a specific course."""
        course_id = random.randint(1, 10)
        self.client.get(f"/api/courses/{course_id}/")
    
    @task(1)
    def attempt_login(self):
        """Attempt to login (will fail)."""
        data = {
            "email": "nonexistent@test.com",
            "password": "wrongpassword"
        }
        self.client.post("/api/users/login/", json=data)


# Event handlers for custom metrics
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when the load test starts."""
    logger.info("Load test starting...")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when the load test stops."""
    logger.info("Load test completed!")
    logger.info(f"Total requests: {environment.stats.total.num_requests}")
    logger.info(f"Total failures: {environment.stats.total.num_failures}")
    logger.info(f"Average response time: {environment.stats.total.avg_response_time}ms")
    logger.info(f"RPS: {environment.stats.total.total_rps}")


# Run with:
# locust -f tests/load_test.py --host=http://localhost:8000
# Then open http://localhost:8089 to configure and start the test