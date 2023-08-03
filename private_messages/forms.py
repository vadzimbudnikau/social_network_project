from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']
        labels = {
            'content': 'Content'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 10})
        }


