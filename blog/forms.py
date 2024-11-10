from django import forms
from .models import Ticket
from django.utils.translation import gettext as _


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
