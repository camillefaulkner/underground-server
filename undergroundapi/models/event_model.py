from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):

    name = models.CharField(max_length=40)
    image = models.ImageField(
        upload_to='images', height_field=None,
        width_field=None, max_length=None, null=True)
    date = models.DateField()
    time = models.TimeField()
    description= models.CharField(max_length=400)
    venue = models.ForeignKey("Venue", on_delete=models.SET_NULL, null=True, related_name='events')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    artists = models.ManyToManyField("Artist", through="EvtArtist", related_name="events")