from django.shortcuts import render
from . import forms
from .models import Ticket

class FluxView:
    def view(request):
        message = ""

        return render(
            request,
            "blog/flux.html",
            context={"message": message},
        )


class TicketView:
    def create_ticket_page(request):
        form = forms.TicketForm()
        message = ""
        
        if request.method == "POST":
            form = forms.TicketForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    Ticket.objects.create(
                        title = form.cleaned_data["title"],
                        description = form.cleaned_data["description"],
                        user = request.user,
                        image = form.cleaned_data["image"],
                    )
                except:
                    message = "Quelque chose n'a pas fonctionné. Veuillez contacter votre administrateur."
                else:
                    message = "✅ Ticket créé avec succès."

        return render(
            request,
            "blog/ticket.html",
            context={"form": form, "message": message},
        )
# Different approach, better ? 
# https://stackoverflow.com/questions/680770/django-imagefield-not-working-properly-via-modelform


class PostsView:
    def posts_view_page(request):
        message = ""

        return render(
            request,
            "blog/posts.html",
            context={"message": message},
        )


class AbonnementView:
    def abonnement_view_page(request):
        message = ""

        return render(
            request,
            "blog/abonnement.html",
            context={"message": message},
        )


class CritiqueView:
    def create_critique_page(request):
        message = ""

        return render(
            request,
            "blog/critique.html",
            context={"message": message},
        )
