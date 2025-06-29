from django import forms
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class signup_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class login_form(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)

class add_note_form(forms.ModelForm):
      class Meta:
        model = Note
        fields = ['title', 'content', 'type', 'privacy']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your note content here...'
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. personal, work'
            }),
            'privacy': forms.Select(attrs={
                'class': 'form-control'
            })
        }