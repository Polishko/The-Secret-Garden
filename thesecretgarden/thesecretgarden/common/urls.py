
from django.urls import path

from thesecretgarden.common.views import landing_page, ContactUsView, AboutUs, ContactMessageApiView, custom_404_view, \
    related_products

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('about-us/', AboutUs.as_view(), name='about-us'),
    path('api/contact/', ContactMessageApiView.as_view(), name='contact-api'),
    path('api/related-products/<str:product_type>/', related_products, name='related-products'),
    path('simulate-404/', custom_404_view, name='simulate-404'),  # Used for custom 404 simulation
]
