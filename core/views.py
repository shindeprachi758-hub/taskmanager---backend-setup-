from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Task  # assuming Task model exists

from .models import Project, Task
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    UserSerializer,
    RegisterSerializer,
    ChangePasswordSerializer
)

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'home.html', {'tasks': tasks})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'User Registered Successfully!')
        return redirect('login')
    return render(request, 'register.html')

def dashboard(request):
    sort_by = request.GET.get("sort", "created_at")  
    status_filter = request.GET.get("status", "all")  

    tasks = Task.objects.filter(user=request.user)

    if status_filter == "completed":
        tasks = tasks.filter(is_completed=True)
    elif status_filter == "pending":
        tasks = tasks.filter(is_completed=False)

    if sort_by == "name":
        tasks = tasks.order_by("title")
    elif sort_by == "recent":
        tasks = tasks.order_by("-created_at")
    else:
        tasks = tasks.order_by("created_at")

    return render(request, "core/dashboard.html", {"tasks": tasks})

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


# ---------------------------------------------------
#   LOGIN VIEW (JWT TOKEN)
# ---------------------------------------------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------
#   USER PROFILE VIEW
# ---------------------------------------------------
class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ---------------------------------------------------
#   CHANGE PASSWORD VIEW
# ---------------------------------------------------
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)