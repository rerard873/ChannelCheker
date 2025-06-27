from django.db import models
from django.conf import settings



class Channels(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=10, choices= [
    ('twitch', 'Twitch'),
    ])
    status = models.CharField(max_length=10, choices=[('online', 'Online'), ('offline', 'Offline')], default='offline')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Videos(models.Model):
    channel = models.ForeignKey(Channels, on_delete=models.CASCADE)
    url = models.URLField()
    name = models.CharField(max_length=100,unique=True)
    published_at = models.DateTimeField()
    type = models.CharField(max_length=10, choices=[
        ('stream', 'Stream'),
        ('video', 'Video'),
    ])
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    def __str__(self):
        return self.name