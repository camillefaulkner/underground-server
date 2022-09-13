from email.mime import image
from django.db import models

class Artist(models.Model):

    name = models.CharField(max_length=30)
    social = models.CharField(max_length=30, null=True)
    image = models.ImageField(
        upload_to='images', height_field=None,
        width_field=None, max_length=None, null=True)
    description = models.CharField(max_length=400)
    spotify = models.URLField(null=True)