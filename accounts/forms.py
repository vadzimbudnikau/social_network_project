from django import forms
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm


class UserProfileForm(forms.ModelForm):
    """
    A form for updating the user profile information.

    Inherits from `forms.ModelForm` and is linked to the `Profile` model.
    Provides fields for 'avatar', 'bio', 'phone_number', 'date_of_birth', 'location', and 'website'.
    Uses custom labels for each field.
    The 'date_of_birth' field is rendered with a date picker widget.

    Attributes:
        model (Profile): The model to link the form to.
        fields (list): The list of fields to include in the form.
        labels (dict): Custom labels for each form field.
        widgets (dict): Custom widgets for each form field.
    """

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone_number', 'date_of_birth', 'location', 'website']
        labels = {
            'avatar': 'Avatar',
            'bio': 'Bio',
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'location': 'Location',
            'website': 'Website'
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom form for changing user password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    new_password2 = forms.CharField(
        label="New Password Confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
