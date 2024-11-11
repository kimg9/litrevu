from django.shortcuts import render
from django.forms.models import modelformset_factory


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
            ticket_form = forms.TicketForm(request.POST, request.FILES)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                
                print(ticket)

                message = "✅ Ticket créé avec succès."

        return render(
            request,
            "blog/ticket.html",
            context={"form": form, "message": message},
        )


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
        ChoiceFormSet = modelformset_factory(
            Ticket, validate_min=True, form=forms.TicketForm
        )

        form = forms.ReviewForm()
        formset = ChoiceFormSet(queryset=Ticket.objects.none())
        message = ""

        if request.method == "POST":
            critique_form = forms.ReviewForm(request.POST)
            ticket_form = ChoiceFormSet(request.POST, request.FILES)

            if all([critique_form.is_valid(), ticket_form.is_valid()]):
                cd = ticket_form.cleaned_data[0]
                ticket = Ticket(
                    title=cd['title'],
                    description=cd['description'],
                    user=request.user,
                    image=cd['image'],
                )
                ticket.save()

                critique = critique_form.save(commit=False)
                critique.ticket = ticket
                critique.user = request.user
                critique.save()

                message = "✅ Critique créée avec succès."

        return render(
            request,
            "blog/critique.html",
            context={"form": form, "formset": formset, "message": message},
        )
