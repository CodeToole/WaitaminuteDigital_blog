from django.urls import path

from . import views

urlpatterns = [
    path('consultation/', views.lead_submit, name='lead_submit'),
]
