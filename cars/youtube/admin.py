from django.contrib import admin
from .models import Playlist, Video, GoogleSettings

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'published_at')

@admin.register(GoogleSettings)
class GoogleSettingsAdmin(admin.ModelAdmin):
    list_display = ('api_key',)