from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', blank=True,
                                  null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username} ({self.timestamp})'


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    messages = models.ManyToManyField(Message)

    def __str__(self):
        return ', '.join([participant.username for participant in self.participants.all()])
