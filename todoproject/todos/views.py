from django.utils import timezone
from datetime import timedelta as timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from django.utils.crypto import constant_time_compare
import os
from .models import Todo, Note, UploadedFile, CodeSnippet, Link, ChatMessage

US_PASSPHRASE_BASE = 'khushii'

ALLOWED_EXTENSIONS = {
    'pdf', 'txt', 'md', 'doc', 'docx', 'xls', 'xlsx',
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg',
    'mp3', 'mp4', 'zip', 'csv',
}
MAX_NOTE_CONTENT = 500_000  # 500 KB


@login_required
def index(request):
    todos = Todo.objects.filter(user=request.user)
    today_start = timezone.make_aware(timezone.datetime.combine(timezone.localdate(), timezone.datetime.min.time()))
    today_end = today_start + timedelta(days=1)
    today_count = Todo.objects.filter(user=request.user, created_at__gte=today_start, created_at__lt=today_end).count()
    return render(request, 'todos/index.html', {'todos': todos, 'today_count': today_count})


@login_required
@require_POST
def add(request):
    title = request.POST.get('title', '').strip()[:200]
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
        title = request.POST.get('title', 'Untitled').strip() or 'Untitled'
        content = request.POST.get('content', '')
        if len(title) > 200:
            return JsonResponse({'error': 'Title too long'}, status=400)
        if len(content) > MAX_NOTE_CONTENT:
            return JsonResponse({'error': 'Content too long'}, status=400)
        note.title = title
        note.content = content
        note.save()
        return JsonResponse({'saved': True, 'updated_at': note.updated_at.strftime('%H:%M:%S')})
    all_notes = Note.objects.filter(user=request.user)
    return render(request, 'todos/note_detail.html', {'note': note, 'all_notes': all_notes})


@login_required
def search(request):
    q = request.GET.get('q', '').strip()[:200]
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


@login_required
def files_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'todos/files.html', {'files': files})


@login_required
@require_POST
def file_upload(request):
    f = request.FILES.get('file')
    if f:
        files = UploadedFile.objects.filter(user=request.user)
        if f.size > 10 * 1024 * 1024:
            return render(request, 'todos/files.html', {'files': files, 'error': 'File exceeds 10 MB limit.'})
        ext = f.name.rsplit('.', 1)[-1].lower() if '.' in f.name else ''
        if ext not in ALLOWED_EXTENSIONS:
            return render(request, 'todos/files.html', {'files': files, 'error': f'File type .{ext} is not allowed.'})
        safe_name = os.path.basename(f.name)
        f.name = safe_name
        UploadedFile.objects.create(user=request.user, file=f, original_name=safe_name, size=f.size)
    return redirect('files_list')


@login_required
def file_download(request, pk):
    from django.http import FileResponse
    uf = get_object_or_404(UploadedFile, pk=pk, user=request.user)
    safe_name = os.path.basename(uf.original_name)
    return FileResponse(uf.file.open('rb'), as_attachment=True, filename=safe_name)


@login_required
@require_POST
def file_delete(request, pk):
    uf = get_object_or_404(UploadedFile, pk=pk, user=request.user)
    uf.file.delete(save=False)
    uf.delete()
    return redirect('files_list')


MAX_SNIPPET_CONTENT = 500_000


@login_required
def code_list(request):
    first = CodeSnippet.objects.filter(user=request.user).first()
    if first:
        return redirect('code_detail', pk=first.pk)
    return render(request, 'todos/code_empty.html')


@login_required
@require_POST
def code_create(request):
    snippet = CodeSnippet.objects.create(user=request.user, title='Untitled', content='')
    return redirect('code_detail', pk=snippet.pk)


@login_required
def code_detail(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled').strip() or 'Untitled'
        language = request.POST.get('language', 'python')
        content = request.POST.get('content', '')
        if len(title) > 200:
            return JsonResponse({'error': 'Title too long'}, status=400)
        if len(content) > MAX_SNIPPET_CONTENT:
            return JsonResponse({'error': 'Content too long'}, status=400)
        valid_languages = {c[0] for c in CodeSnippet.LANGUAGE_CHOICES}
        if language not in valid_languages:
            language = 'text'
        snippet.title = title
        snippet.language = language
        snippet.content = content
        snippet.save()
        return JsonResponse({'saved': True, 'updated_at': snippet.updated_at.strftime('%H:%M:%S')})
    all_snippets = CodeSnippet.objects.filter(user=request.user)
    return render(request, 'todos/code_detail.html', {'snippet': snippet, 'all_snippets': all_snippets})


@login_required
@require_POST
def code_delete(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    snippet.delete()
    return redirect('code_list')


@login_required
def links_list(request):
    tag_filter = request.GET.get('tag', '').strip()
    links = Link.objects.filter(user=request.user)
    if tag_filter:
        links = links.filter(tags__icontains=tag_filter)
    all_tags = []
    for link in Link.objects.filter(user=request.user):
        for t in link.tag_list:
            if t not in all_tags:
                all_tags.append(t)
    return render(request, 'todos/links.html', {
        'links': links,
        'all_tags': sorted(all_tags),
        'tag_filter': tag_filter,
    })


@login_required
@require_POST
def link_add(request):
    url = request.POST.get('url', '').strip()[:2000]
    title = request.POST.get('title', '').strip()[:200]
    description = request.POST.get('description', '').strip()[:1000]
    tags = request.POST.get('tags', '').strip()[:200]
    if url:
        Link.objects.create(
            user=request.user,
            url=url,
            title=title,
            description=description,
            tags=tags,
        )
    return redirect('links_list')


@login_required
@require_POST
def link_delete(request, pk):
    link = get_object_or_404(Link, pk=pk, user=request.user)
    link.delete()
    return redirect('links_list')


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = False

    if request.method == 'POST':
        ip = _get_client_ip(request)
        cache_key = f'login_attempts:{ip}'
        attempts = cache.get(cache_key, 0)

        if attempts >= 5:
            return render(request, 'registration/login.html', {'error': True, 'locked': True})

        password = request.POST.get('password', '')
        today = timezone.localdate().strftime('%d')
        expected = settings.BASE_PASSWORD + today

        if constant_time_compare(password, expected):
            cache.delete(cache_key)
            user = User.objects.first()
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
        else:
            cache.set(cache_key, attempts + 1, 3600)

        error = True

    return render(request, 'registration/login.html', {'error': error})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


# ── Chat ──────────────────────────────────────────────────────────────────────

def us_view(request):
    """Public chat page for her. Protected by passphrase stored in session."""
    if request.method == 'POST':
        entered = request.POST.get('passphrase', '').strip().lower()
        expected = US_PASSPHRASE_BASE + timezone.localdate().strftime('%d')
        if constant_time_compare(entered, expected):
            request.session['us_auth'] = True
            # Mark his messages as read (she's now reading)
            ChatMessage.objects.filter(sender='me', is_read=False).update(is_read=True)
        else:
            return render(request, 'todos/us.html', {'gate': True, 'error': True})
        return redirect('us')

    if not request.session.get('us_auth'):
        return render(request, 'todos/us.html', {'gate': True})

    # Mark his unread messages as read since she opened the chat
    ChatMessage.objects.filter(sender='me', is_read=False).update(is_read=True)
    messages = ChatMessage.objects.all()
    return render(request, 'todos/us.html', {'gate': False, 'messages': messages})


@require_POST
def us_send(request):
    """Her sends a message."""
    if not request.session.get('us_auth'):
        return JsonResponse({'error': 'unauthorized'}, status=403)
    content = request.POST.get('content', '').strip()[:2000]
    if content:
        msg = ChatMessage.objects.create(content=content, sender='her')
        return JsonResponse({
            'id': str(msg.pk),
            'content': msg.content,
            'sender': msg.sender,
            'time': msg.sent_at.strftime('%I:%M %p'),
            'ts': msg.sent_at.timestamp(),
        })
    return JsonResponse({'error': 'empty'}, status=400)


def us_poll(request):
    """Returns new messages since a given timestamp (epoch seconds). For her page polling."""
    if not request.session.get('us_auth'):
        return JsonResponse({'error': 'unauthorized'}, status=403)
    after_ts = request.GET.get('after', None)
    qs = ChatMessage.objects.all()
    if after_ts:
        try:
            from datetime import datetime as dt
            ts = dt.fromtimestamp(float(after_ts), tz=timezone.utc)
            qs = qs.filter(sent_at__gt=ts)
        except (ValueError, OSError):
            pass
    # Also mark his messages as read
    ChatMessage.objects.filter(sender='me', is_read=False).update(is_read=True)
    data = [{'id': str(m.pk), 'content': m.content, 'sender': m.sender,
             'time': m.sent_at.strftime('%I:%M %p'),
             'ts': m.sent_at.timestamp()} for m in qs]
    return JsonResponse({'messages': data})


@login_required
def chats_view(request):
    """His chat inbox. Marks all her messages as read."""
    ChatMessage.objects.filter(sender='her', is_read=False).update(is_read=True)
    messages = ChatMessage.objects.all()
    return render(request, 'todos/chats.html', {'messages': messages})


@login_required
@require_POST
def chats_send(request):
    """He sends a reply."""
    content = request.POST.get('content', '').strip()[:2000]
    if content:
        msg = ChatMessage.objects.create(content=content, sender='me')
        return JsonResponse({
            'id': str(msg.pk),
            'content': msg.content,
            'sender': msg.sender,
            'time': msg.sent_at.strftime('%I:%M %p'),
        })
    return JsonResponse({'error': 'empty'}, status=400)


@login_required
def chats_poll(request):
    """Returns new messages since a given timestamp for his page polling."""
    after_ts = request.GET.get('after', None)
    qs = ChatMessage.objects.all()
    if after_ts:
        try:
            from datetime import datetime as dt
            ts = dt.fromtimestamp(float(after_ts), tz=timezone.utc)
            qs = qs.filter(sent_at__gt=ts)
        except (ValueError, OSError):
            pass
    # Mark her new messages as read since he's polling
    ChatMessage.objects.filter(sender='her', is_read=False).update(is_read=True)
    data = [{'id': str(m.pk), 'content': m.content, 'sender': m.sender,
             'time': m.sent_at.strftime('%I:%M %p'),
             'ts': m.sent_at.timestamp()} for m in qs]
    return JsonResponse({'messages': data})
