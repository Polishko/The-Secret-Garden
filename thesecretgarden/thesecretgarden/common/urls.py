from django.urls import path

from thesecretgarden.common.views import show_home_page

urlpatterns = [
    path('', show_home_page, name='landing-page')
]
