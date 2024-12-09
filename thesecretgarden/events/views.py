from django.views.generic import TemplateView

class ComingSoonView(TemplateView):
    template_name = 'events/coming_soon.html'
