"""
URL patterns for user authentication and profile management.
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    # Profile
    path('profile/', views.get_current_user, name='profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('password/change/', views.change_password, name='change-password'),
    
    # Learning Style Assessment
    path('assessment/', views.LearningStyleAssessmentView.as_view(), name='assessment'),
    path('assessment/history/', views.LearningStyleAssessmentListView.as_view(), name='assessment-history'),
    
    # Preferences
    path('preferences/', views.UserPreferencesView.as_view(), name='preferences'),
    
    # User List
    path('list/', views.UserListView.as_view(), name='user-list'),
]