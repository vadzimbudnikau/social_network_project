from django.urls import path
from . import views

app_name = 'private_messages'

urlpatterns = [
    path('send/', views.SendMessageView.as_view(), name='send_message'),
    path('send/<int:recipient_id>/', views.SendMessageView.as_view(), name='send_message_to'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('sent/', views.SentView.as_view(), name='sent'),
]
