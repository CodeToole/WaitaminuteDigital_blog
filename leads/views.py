from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from .forms import LeadForm
from .models import Lead


def lead_submit(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    honeypot = request.POST.get('website') or request.POST.get('company')
    if honeypot:
        return render(request, 'leads/partials/consultation_success.html', {'ignored': True})

    form = LeadForm(request.POST)
    if form.is_valid():
        lead = Lead.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data.get('phone', ''),
            business_name=form.cleaned_data.get('business_name', ''),
            preferred_contact=form.cleaned_data['preferred_contact'],
            message=form.cleaned_data['message'],
            source='services_page',
        )
        return render(request, 'leads/partials/consultation_success.html', {'lead': lead})

    return render(request, 'leads/partials/consultation_form.html', {'form': form})
