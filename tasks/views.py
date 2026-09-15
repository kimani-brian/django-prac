from django.shortcuts import redirect, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .forms import TaskForm
from .serializers import TaskSerializer

def home(request):
    # If the user isn't logged in, redirect them to the login page
    if not request.user.is_authenticated:
        return redirect('login') # Or wherever your login page is

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # FIX: Use commit=False to assign the user before saving
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('home')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/home.html', {'tasks': tasks, 'form': form})

class TaskList(APIView):
    # This ensures only logged-in users can access the API
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # Filter by the logged-in user
        tasks = Task.objects.filter(user=request.user) 
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)