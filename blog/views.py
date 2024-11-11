from django.shortcuts import render
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
            context={"form": form, "message": message},
        )


# https://stackoverflow.com/questions/680770/django-imagefield-not-working-properly-via-modelform


class PostsView:
    def posts_view_page(request):
        message = ""

        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

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
