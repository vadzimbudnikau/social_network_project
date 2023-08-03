# private_messages/context_processors.py

from .models import Message


def unread_message_count(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
    return {'unread_message_count': unread_count}
