from django import forms
from .models import Order
from django.utils.translation import gettext_lazy as _

class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'city']
        labels = {
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
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }