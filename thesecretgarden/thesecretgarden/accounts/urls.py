from django.contrib.auth.views import LogoutView
from django.urls import path, include

from thesecretgarden.accounts.forms import ProfileEditForm
from thesecretgarden.accounts.views import AppUserRegisterView, AppUserLoginView, ProfileDetailsView, ProfileEditView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<slug:slug>/', include([
        path('', ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
    ])),
]
