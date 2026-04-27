"""
Forms for the Quest Manager Game application.

Includes forms for:
- User registration
- Character creation and editing
- Quest creation and editing (admin only)
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Character, Quest


# ---------------------------------------------------------------------------
# User Registration Form
# ---------------------------------------------------------------------------
class RegisterForm(UserCreationForm):
    """
    Extended user registration form with email field.
    Uses Django's built-in UserCreationForm for secure password hashing.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        """Save user with email."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# ---------------------------------------------------------------------------
# Character Form
# ---------------------------------------------------------------------------
class CharacterForm(forms.ModelForm):
    """
    Form for creating and editing a player's character.
    Players can set the name and class; XP is managed by the system.
    """

    class Meta:
        model = Character
        fields = ['name', 'character_class']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter character name',
                'maxlength': 100,
            }),
            'character_class': forms.Select(attrs={
                'class': 'form-input',
            }),
        }
        labels = {
            'name': 'Character Name',
            'character_class': 'Character Class',
        }


# ---------------------------------------------------------------------------
# Quest Form (Admin Only)
# ---------------------------------------------------------------------------
class QuestForm(forms.ModelForm):
    """
    Form for creating and editing quests.
    Only accessible by admin users.
    XP rewards are automatically determined by difficulty.
    """

    class Meta:
        model = Quest
        fields = ['title', 'description', 'difficulty', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter quest title',
                'maxlength': 200,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Describe the quest objectives...',
                'rows': 5,
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-input',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }
        labels = {
            'title': 'Quest Title',
            'description': 'Quest Description',
            'difficulty': 'Difficulty Level',
            'is_active': 'Active (available to players)',
        }
