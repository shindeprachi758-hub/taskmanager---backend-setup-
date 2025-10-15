from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Project, Task
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer
)

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only show logged-in user's projects
        return Project.objects.filter(owner=self.request.user)

class TasklistCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        project_id = self.request.query_params.get('project')  # Filter tasks by project
        if project_id:
            return Task.objects.filter(owner=self.request.user, project_id=project_id)
        # only show logged-in user's tasks
        return Task.objects.filter(owner=self.request.user)
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # only show logged-in user's tasks
        return Task.objects.filter(owner=self.request.user)

# ---------------------------------------------------
#   PROJECT & TASK API VIEWSETS
# ---------------------------------------------------
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]  # For now allow all (no login required)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------------------------------
#   USER REGISTRATION API
# ---------------------------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class ProjectListView(APIView):
    def get(self, request):
        return Response({"message": "List of projects"})

class TaskListView(APIView):
    def get(self, request):
        return Response({"message": "List of tasks"})