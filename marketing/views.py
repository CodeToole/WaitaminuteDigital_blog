from django.shortcuts import render

from leads.forms import LeadForm


def home_page(request):
    return render(request, 'core/home.html')


def about_page(request):
    return render(request, 'marketing/about_page.html')


def services_page(request):
    return render(request, 'services/services.html', {'form': LeadForm()})
