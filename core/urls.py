# core/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import ProjectListCreateView, ProjectDetailView
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
    # CRUD Endpoints for Projects and Tasks
    path('', include(router.urls)),

    # JWT Token authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom Authentication API endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
]