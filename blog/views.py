from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory

from . import forms
from .models import Review, Ticket


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
        title = "Créer un ticket"
        message = ""

        if request.method == "POST":
            ticket_form = forms.TicketForm(request.POST, request.FILES)
            if ticket_form.is_valid():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

                message = "✅ Ticket créé avec succès."

        return render(
            request,
            "blog/ticket.html",
            context={"form": form, "title": title, "message": message},
        )

    def update_ticket_page(request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        form = forms.TicketForm(instance=ticket)
        title = "Modifier un ticket"
        message = ""

        if request.method == "POST":
            ticket_form = forms.TicketForm(request.POST, instance=ticket)
            if ticket_form.is_valid():
                ticket_form.save()
                return redirect("posts")

        return render(
            request,
            "blog/ticket.html",
            context={"form": form, "title": title, "message": message},
        )

    def delete_ticket_page(request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        message = ""

        if request.method == "POST":
            if request.user == ticket.user:
                ticket.delete()
                return redirect("posts")
            else:
                message = "Vous n'avez pas l'autorisation de supprimer un ticket d'un autre utilisateur."

        return render(
            request,
            "blog/confirmation_page.html",
            context={"post": ticket, "message": message},
        )


class PostsView:
    def posts_view_page(request):
        message = ""

        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        for review in reviews:
            print(review.pk)

        star_rating = ""
        for review in reviews:
            for _ in range(review.rating):
                star_rating += "★"
            review.rating = star_rating

        posts = list(tickets) + list(reviews)
        sorted_posts = sorted(posts, key=lambda k: k.time_created, reverse=True)

        return render(
            request,
            "blog/posts.html",
            context={"message": message, "posts": sorted_posts},
        )


class AbonnementView:
    def abonnement_view_page(request):
        message = ""

        return render(
            request,
            "blog/abonnement.html",
            context={"message": message},
        )


class ReviewView:
    def create_review_page(request):
        ChoiceFormSet = modelformset_factory(
            Ticket, validate_min=True, form=forms.TicketForm
        )

        form = forms.ReviewForm()
        formset = ChoiceFormSet(queryset=Ticket.objects.none())
        message = ""

        if request.method == "POST":
            review_form = forms.ReviewForm(request.POST)
            ticket_form = ChoiceFormSet(request.POST, request.FILES)

            if all([review_form.is_valid(), ticket_form.is_valid()]):
                cd = ticket_form.cleaned_data[0]
                ticket = Ticket(
                    title=cd["title"],
                    description=cd["description"],
                    user=request.user,
                    image=cd["image"],
                )
                ticket.save()

                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = request.user
                review.save()

                message = "✅ Critique créée avec succès."

        return render(
            request,
            "blog/reviews/create_review.html",
            context={"form": form, "formset": formset, "message": message},
        )

    def update_review_page(request, pk):
        review = get_object_or_404(Review, pk=pk)
        ticket = review.ticket
        form = forms.ReviewForm(instance=review)
        message = ""

        if request.method == "POST":
            review_form = forms.ReviewForm(request.POST, instance=review)

            if review_form.is_valid():
                review_form.save()
                return redirect("posts")

        return render(
            request,
            "blog/reviews/update_review.html",
            context={
                "form": form,
                "ticket": ticket,
                "message": message,
            },
        )

    def delete_review_page(request, pk):
        review = get_object_or_404(Review, pk=pk)
        message = ""

        if request.method == "POST":
            if request.user == review.user:
                review.delete()
                return redirect("posts")
            else:
                message = "Vous n'avez pas l'autorisation de supprimer une critique d'un autre utilisateur."

        return render(
            request,
            "blog/confirmation_page.html",
            context={"post": review, "message": message},
        )
