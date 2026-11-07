from django.contrib import admin
from .models import SiteConfig, LeadershipProfile, Club, Event, PressRelease


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Impact Tracker Numbers', {
            'fields': ('total_clubs', 'total_members', 'volunteer_hours')
        }),
        ('Hero Section', {
            'fields': ('hero_tagline', 'hero_subtext', 'president_theme')
        }),
    )

    def has_add_permission(self, request):
        # Enforce singleton
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LeadershipProfile)
class LeadershipProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'role_level', 'order')
    list_filter = ('role_level',)
    search_fields = ('full_name', 'title')
    list_editable = ('order',)
    ordering = ('role_level', 'order')


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'zone', 'club_type', 'president_name')
    list_filter = ('region', 'zone', 'club_type')
    search_fields = ('name', 'president_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'is_draft', 'president_attending')
    list_filter = ('category', 'is_draft', 'president_attending')
    search_fields = ('title',)
    list_editable = ('is_draft', 'president_attending')
    date_hierarchy = 'start_time'


@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_featured')
    list_editable = ('is_featured',)
    date_hierarchy = 'published_at'
