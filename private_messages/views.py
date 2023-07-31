from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Message
from .forms import MessageForm


class SendMessageView(LoginRequiredMixin, View):
    template_name = 'private_messages/send_message.html'
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        recipient_id = request.GET.get('receiver')
        form = self.form_class(initial={'recipient': recipient_id})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('private_messages:inbox')

        return render(request, self.template_name, {'form': form})


class InboxView(LoginRequiredMixin, ListView):
    """View for displaying the inbox of the authenticated user."""
    model = Message
    template_name = 'private_messages/inbox.html'
    context_object_name = 'inbox'
    paginate_by = 10

    def get_queryset(self):
        # Фильтруем сообщения по получателю (recipient)
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')


class SentView(LoginRequiredMixin, ListView):
    """View for displaying the sent messages of the authenticated user."""
    model = Message
    template_name = 'private_messages/sent.html'
    context_object_name = 'sent_messages'
    paginate_by = 10

    def get_queryset(self):
        # Фильтруем сообщения по отправителю (sender)
        return Message.objects.filter(sender=self.request.user).order_by('-timestamp')
