from django.urls import path

from thesecretgarden.common.views import landing_page, ContactUsView, AboutUs, ContactMessageApiView

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('about-us/', AboutUs.as_view(), name='about-us'),
    path('api/contact/', ContactMessageApiView.as_view(), name='contact-api'),
]
