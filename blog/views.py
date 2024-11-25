from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.views.generic import ListView

from authentification.models import User
from . import forms
from .models import Review, Ticket, UserFollows

def set_stars(reviews):
    star_rating = ""
    for review in reviews:
        for _ in range(review.rating):
            star_rating += "★"
        review.rating = star_rating
    return reviews

class PostsView:
    def posts_view_page(request):
        message = ""

        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)

        reviews = set_stars(reviews)

        posts = list(tickets) + list(reviews)
        sorted_posts = sorted(posts, key=lambda k: k.time_created, reverse=True)

        return render(
            request,
            "blog/posts.html",
            context={"message": message, "posts": sorted_posts},
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


class AbonnementView:
    def abonnement_view_page(request):
        follows = UserFollows.objects.filter(user=request.user)
        followed_by = UserFollows.objects.filter(followed_user=request.user)
        message = ""
        

        if 'search' in request.POST:
            searched_username = request.POST['search']
            try:
                followed_user = User.objects.get(username=searched_username)
            except User.DoesNotExist:
                message = "L'utilisateur recherché n'existe pas."
            else:
                UserFollows.objects.create(
                    user=request.user,
                    followed_user=followed_user
                )
        elif 'unsubscribe' in request.POST:
            followed_user = request.POST['unsubscribe']
            user_follow = get_object_or_404(UserFollows, user=request.user, followed_user_id=followed_user)
            user_follow.delete()

        return render(
            request,
            "blog/abonnement.html",
            context={"message": message, "follows": follows, "followed_by": followed_by},
        )

class FluxView(ListView):
    def get(self, request):
        message = ""
        
        all_users = list(UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True))
        all_users.append(request.user.id)
        print(all_users)
        tickets = Ticket.objects.filter(user__in=all_users)
        reviews = Review.objects.filter(user__in=all_users)

        reviews = set_stars(reviews)

        posts = list(tickets) + list(reviews)
        sorted_posts = sorted(posts, key=lambda k: k.time_created, reverse=True)

        return render(
            request,
            "blog/posts.html",
            context={"message": message, "posts": sorted_posts, "flux": True},

        )