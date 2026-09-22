from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .forms import TaskForm
from .serializers import TaskSerializer

def home(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Create the object but don't save to DB yet
            task = form.save(commit=False)
            # Assign the current logged-in user
            task.user = request.user 
            # Now save to DB
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    # Filter by user so they only see their own tasks
    tasks = Task.objects.filter(user=request.user) 
    return render(request, 'tasks/home.html', {'tasks': tasks, 'form': form})

def delete_task(request, pk):
    # Find the task or return 404 error if it doesn't exist
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('home')

def toggle_task(request, pk):
    # Find the task belonging to the logged-in user
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    # Flip the boolean value (True becomes False, False becomes True)
    task.completed = not task.completed
    task.save()
    
    return redirect('home')

class TaskList(APIView):
    # This ensures only logged-in users can access the API
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # Filter by the logged-in user
        tasks = Task.objects.filter(user=request.user) 
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)