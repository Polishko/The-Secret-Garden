from django.contrib.auth.views import LogoutView
from django.urls import path

from thesecretgarden.accounts.views import AppUserRegisterView, AppUserLoginView, ProfileDetailsView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<slug:slug>/', ProfileDetailsView.as_view(), name='profile-details')
]
