from django import forms
from django.forms.models import modelformset_factory

from .models import Ticket
from .models import Review
from .models import UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]

    rating = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=((0, "-0"), (1, "-1"), (2, "-2"), (3, "-3"), (4, "-4"), (5, "-5")),
    )
