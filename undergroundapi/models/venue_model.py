from django.db import models
from django.contrib.auth.models import User

class Venue(models.Model):

    name = models.CharField(max_length=30)
    address = models.CharField(max_length=70)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, related_name='venues')
    private = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)