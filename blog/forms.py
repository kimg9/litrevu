from django import forms
from django.forms.models import modelformset_factory

from .models import Ticket
from .models import Review
from .models import UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.image:
            # Ajoute un champ HTML pour afficher l'image actuelle
            self.fields['image'].label = (
                f'<b>Image*</b> </br> <img src="{self.instance.image.url}" alt="Image actuelle" '
                f'style="max-width: 200px; max-height: 200px;" />'
            )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]

    rating = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=((0, "-0"), (1, "-1"), (2, "-2"), (3, "-3"), (4, "-4"), (5, "-5")),
    )
