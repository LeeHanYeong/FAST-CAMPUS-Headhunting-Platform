from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import ApplicantUser, User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
        })
        self.base_fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
        })
        super().__init__(*args, **kwargs)

    class Meta:
        widgets = {
            'username': forms.TextInput({
                'attrs': {
                    'class': 'form-control',
                }
            })
        }
