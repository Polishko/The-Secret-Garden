from django.shortcuts import render


def show_home_page(request):
    return render(request, 'common/landing-page.html')

