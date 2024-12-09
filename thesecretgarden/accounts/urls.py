from django.contrib.auth.views import LogoutView
from django.urls import path, include

from thesecretgarden.accounts.views import AppUserRegisterView, AppUserLoginView, ProfileDetailsView, ProfileEditView, \
    ProfileDeactivateView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<slug:slug>/', include([
        path('', ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('deactivate/', ProfileDeactivateView.as_view(), name='profile-deactivate'),
    ])),
]
