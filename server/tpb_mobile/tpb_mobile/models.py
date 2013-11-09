from django.db import models

class Torrent(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    magnet_link = models.CharField(max_length=1000)
    torrent_link = models.CharField(max_length=1000)
    size = models.CharField(max_length=20)