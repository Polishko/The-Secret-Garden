from django.shortcuts import render


def landing_page(request):
    return render(request, 'common/landing-page.html', {'is_landing_page': True})

