from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Form for creating and updating a post.
    """

    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating a comment.
    """

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'cols': 10})
        }
