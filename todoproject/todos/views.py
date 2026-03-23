from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Q
from .models import Todo, Note


@login_required
def index(request):
    todos = Todo.objects.filter(user=request.user)
    today_count = Todo.objects.filter(user=request.user, created_at__date=date.today()).count()
    return render(request, 'todos/index.html', {'todos': todos, 'today_count': today_count})


@login_required
@require_POST
def add(request):
    title = request.POST.get('title', '').strip()
    if title:
        Todo.objects.create(title=title, user=request.user)
    return redirect('index')


@login_required
@require_POST
def toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('index')


@login_required
@require_POST
def delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect('index')


@login_required
def notes_list(request):
    first = Note.objects.filter(user=request.user).first()
    if first:
        return redirect('note_detail', pk=first.pk)
    return render(request, 'todos/notes_empty.html')


@login_required
@require_POST
def note_create(request):
    note = Note.objects.create(user=request.user, title='Untitled', content='')
    return redirect('note_detail', pk=note.pk)


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title', 'Untitled').strip() or 'Untitled'
        note.content = request.POST.get('content', '')
        note.save()
        return JsonResponse({'saved': True, 'updated_at': note.updated_at.strftime('%H:%M:%S')})
    all_notes = Note.objects.filter(user=request.user)
    return render(request, 'todos/note_detail.html', {'note': note, 'all_notes': all_notes})


@login_required
def search(request):
    q = request.GET.get('q', '').strip()
    notes = []
    todos = []
    if q:
        notes = Note.objects.filter(user=request.user).filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )
        todos = Todo.objects.filter(user=request.user, title__icontains=q)
    return render(request, 'todos/search.html', {'q': q, 'notes': notes, 'todos': todos})


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    return redirect('notes_list')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = False

    if request.method == 'POST':
        password = request.POST.get('password', '')
        today = date.today().strftime('%d')
        expected = settings.BASE_PASSWORD + today
        if password == expected:
            user = User.objects.first()
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
        error = True

    return render(request, 'registration/login.html', {'error': error})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')
