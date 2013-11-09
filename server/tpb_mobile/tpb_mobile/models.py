from django.db import models
from django.contrib.auth.models import User
import settings as s

class Torrent(models.Model):
    user = models.ForeignKey(User, null=True)
    status = models.IntegerField()
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    magnet_link = models.CharField(max_length=1000)
    torrent_link = models.CharField(max_length=1000)
    size = models.CharField(max_length=20)
    seeders = models.IntegerField(null=True)