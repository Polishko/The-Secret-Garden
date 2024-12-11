from django.views.generic import TemplateView

class ComingSoonView(TemplateView):
    """Displays the coming_soon template for planned events page"""
    template_name = 'events/coming_soon.html'
