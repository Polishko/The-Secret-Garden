from django.urls import path

from thesecretgarden.common.views import landing_page

urlpatterns = [
    path('', landing_page, name='landing-page')
]
