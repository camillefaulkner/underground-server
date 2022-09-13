from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from undergroundapi.models import ChosenShow, Event, Artist
from datetime import date, datetime, timedelta

from undergroundapi.models.evt_artist_model import EvtArtist




class EvtArtistView(ViewSet):
    """Rater events view"""



    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        event = Event.objects.get(pk=request.data["event"])
        artist = Artist.objects.get(pk=request.data["artist"])

        connection = EvtArtist.objects.create(
            event = event,
            artist = artist
        )
        serializer = EvtArtistSerializer(connection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EvtArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = EvtArtist
        fields = ('id', 'event', 'artist')
        depth = 1