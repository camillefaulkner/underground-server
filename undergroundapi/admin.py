from django.contrib import admin
from .models import Event, Artist

# Register your models here.
admin.site.register(Artist)
admin.site.register(Event)