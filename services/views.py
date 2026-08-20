from django.shortcuts import render

from leads.forms import LeadForm


def services_page(request):
    return render(request, 'services/services.html', {'form': LeadForm()})
