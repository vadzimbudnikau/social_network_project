from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    """
    Represents a private message sent between users.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', blank=True,
                                  null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the message.
        """
        return f'{self.sender.username} -> {self.recipient.username} ({self.timestamp})'


class Conversation(models.Model):
    """
    Represents a conversation between participants containing messages.
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    messages = models.ManyToManyField(Message)

    def __str__(self):
        """
        Return a string representation of the conversation.
        """
        return ', '.join([participant.username for participant in self.participants.all()])
