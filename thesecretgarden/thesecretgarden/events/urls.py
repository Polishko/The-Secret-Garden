from django.urls import path
from thesecretgarden.events.views import ComingSoonView

urlpatterns = [
    path('', ComingSoonView.as_view(), name='events-coming-soon'),
]
