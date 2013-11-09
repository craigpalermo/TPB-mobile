from django.contrib import admin
from models import Torrent, UserProfile

class TorrentAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'magnet_link', 'torrent_link', 'size')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'uuid', 'client_id')
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Torrent, TorrentAdmin)
