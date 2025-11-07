# core/urls.py

from django.urls import path, include
from rest_framework import routers
from . import views
from .views import ProjectListCreateView, ProjectDetailView, TasklistCreateView, TaskDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import (
    ProjectViewSet,
    TaskViewSet,
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView
)

# -------------------------------
# Routers for Project & Task API
# -------------------------------
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

# -------------------------------
# URL Patterns
# -------------------------------
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # CRUD Endpoints for Projects and Tasks
    path('', include(router.urls)),
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('tasks/', views.TasklistCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # JWT Token authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom Authentication API endpoints
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('tasks/', views.TasklistCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
]