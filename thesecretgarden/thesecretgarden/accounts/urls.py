from django.urls import path

from thesecretgarden.accounts.views import AppUserRegisterView, AppUserLoginView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
]
