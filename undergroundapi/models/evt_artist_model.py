from django.db import models


class EvtArtist(models.Model):

    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
