from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'address', 'phone', 'city')
        labels = {
            'username': _('username'),
            'password': _('password'),
            'first_name': _('first_name'),
            'last_name': _('last_name'),
            'phone': _('phone'),
            'email': _('email'),
            'address': _('address'),
            'city': _('city'),
        }
        help_texts = {
            'email': _('youremail@domain.com'),
        }


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label=_('password'))
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': _('username'),
            'password': _('password'),
        }