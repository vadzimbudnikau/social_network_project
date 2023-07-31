from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .models import Message
from .forms import MessageForm


class SendMessageView(LoginRequiredMixin, View):
    """
    View for sending a private message.

    Requires the user to be logged in. Allows composing and sending messages to other users.

    Attributes:
        template_name (str): The template name for rendering the send message page.
        form_class (MessageForm): The form class for creating the message.

    Methods:
        get(self, request, *args, **kwargs): Handles GET requests for sending a message.
        post(self, request, *args, **kwargs): Handles POST requests for sending a message.
    """

    template_name = 'private_messages/send_message.html'
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for sending a message.

        If the 'receiver' query parameter is provided in the URL, pre-fill the message form with the recipient's ID.

        Args:
            request (HttpRequest): The HTTP GET request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response with the send message form.
        """
        recipient_id = request.GET.get('receiver')
        form = self.form_class(initial={'recipient': recipient_id})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for sending a message.

        Validate the message form, save the message, and redirect to the inbox on successful message sending.

        Args:
            request (HttpRequest): The HTTP POST request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response after handling the POST request.
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('private_messages:inbox')

        return render(request, self.template_name, {'form': form})


class InboxView(LoginRequiredMixin, ListView):
    """
    View for displaying the inbox of the authenticated user.

    Requires the user to be logged in. Displays the received messages of the authenticated user.

    Attributes:
        model (Message): The Message model class.
        template_name (str): The template name for rendering the inbox page.
        context_object_name (str): The context variable name for the inbox messages list.
        paginate_by (int): The number of messages to display per page.

    Methods:
        get_queryset(self): Get the list of messages filtered by recipient.
    """

    model = Message
    template_name = 'private_messages/inbox.html'
    context_object_name = 'inbox'
    paginate_by = 10

    def get_queryset(self):
        """
        Get the list of messages filtered by recipient.

        Returns:
            QuerySet: The filtered messages queryset.
        """
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')


class SentView(LoginRequiredMixin, ListView):
    """
    View for displaying the sent messages of the authenticated user.

    Requires the user to be logged in. Displays the sent messages of the authenticated user.

    Attributes:
        model (Message): The Message model class.
        template_name (str): The template name for rendering the sent messages page.
        context_object_name (str): The context variable name for the sent messages list.
        paginate_by (int): The number of messages to display per page.

    Methods:
        get_queryset(self): Get the list of messages filtered by sender.
    """

    model = Message
    template_name = 'private_messages/sent.html'
    context_object_name = 'sent_messages'
    paginate_by = 10

    def get_queryset(self):
        """
        Get the list of messages filtered by sender.

        Returns:
            QuerySet: The filtered messages queryset.
        """
        return Message.objects.filter(sender=self.request.user).order_by('-timestamp')
