from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'business_name', 'preferred_contact', 'created')
    search_fields = ('name', 'email', 'business_name', 'message')
    list_filter = ('preferred_contact', 'source')
