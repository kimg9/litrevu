from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from authentification.models import User
from . import forms


def login_page(request):
    form = forms.LoginForm()
    message = ""
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                message = f"Bonjour, {user.username}! Vous êtes connecté."
            else:
                message = "Identifiants invalides."
    return render(
        request,
        "authentification/login.html",
        context={"form": form, "message": message},
    )


def logout_user(request):
    logout(request)
    return redirect("login")


def inscription_user(request):
    form = forms.InscriptionForm()
    message = ""
    if request.method == "POST":
        form = forms.InscriptionForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                message = (
                    "Utilisateur créé avec succès !"
                )
            else:
                message = "Une erreur est survenue. Contactez l'administrateur du site."
    return render(
        request,
        "authentification/inscription.html",
        context={"form": form, "message": message},
    )
