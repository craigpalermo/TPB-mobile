from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    uuid = UUIDField(primary_key=True)
    client_id = models.CharField(max_length=50, null=True)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Torrent(models.Model):
    '''
    represents a torrent that the user has in their download queue
    '''
    user = models.ForeignKey(User, null=True)
    status = models.IntegerField()
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    magnet_link = models.CharField(max_length=1000)
    torrent_link = models.CharField(max_length=1000)
    size = models.CharField(max_length=20)
    seeders = models.PositiveIntegerField(null=True)