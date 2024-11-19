"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

import authentification.views as auth
import blog.views as blog

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth.LoginView.login_page, name="login"),
    path("logout/", auth.LogoutView.logout_user, name="logout"),
    path("inscription/", auth.InscriptionView.inscription_user, name="inscription"),
    path("flux/", blog.FluxView.view, name="flux"),
    path("posts/", blog.PostsView.posts_view_page, name="posts"),
    path("abonnements/", blog.AbonnementView.abonnement_view_page, name="abonnements"),
    path("tickets/", blog.TicketView.create_ticket_page, name="tickets"),
    path("reviews/", blog.ReviewView.create_review_page, name="reviews"),
    path('review/<pk>/update', blog.ReviewView.update_review_page, name="update_review_page"),
    path('ticket/<pk>/update', blog.TicketView.update_ticket_page, name="update_ticket_page"),
    path('review/<pk>/delete', blog.ReviewView.delete_review_page, name="delete_review_page"),
    path('ticket/<pk>/delete', blog.TicketView.delete_ticket_page, name="delete_ticket_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
