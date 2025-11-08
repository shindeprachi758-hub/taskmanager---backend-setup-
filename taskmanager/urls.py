"""
URL configuration for taskmanger project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers , permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
from core.views import (

    ProjectViewSet,
    TaskViewSet,
    RegisterView,
    LoginView,
    ProfileView,
    ChangePasswordView
)

# -------------------------------
#  Router for Project & Task
# -------------------------------
router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

schema_view = get_schema_view(
   openapi.Info(
      title="Task Management API",
      default_version='v1',
      description="API documentation for Task Management System",
      contact=openapi.Contact(email="shindeprachi758@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# -------------------------------
#  URL Patterns
# -------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),


    # Projects & Tasks CRUD
    path('api/', include(router.urls)),

    # JWT Token endpoints (from SimpleJWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Custom Authentication Endpoints (Task 2)
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    path('api/auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]