from .models import ChatMessage


def unread_chat_count(request):
    if request.user.is_authenticated:
        count = ChatMessage.objects.filter(sender='her', is_read=False).count()
        return {'unread_chat_count': count}
    return {'unread_chat_count': 0}
