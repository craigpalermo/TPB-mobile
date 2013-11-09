from django.contrib import admin
from models import Torrent

class TorrentAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'magnet_link', 'torrent_link', 'size')

admin.site.register(Torrent, TorrentAdmin)
