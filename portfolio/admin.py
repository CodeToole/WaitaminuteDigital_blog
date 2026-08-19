from django.contrib import admin

from .models import Project, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'is_featured', 'created')
    list_filter = ('is_featured', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'summary', 'client')
    filter_horizontal = ('tags',)
