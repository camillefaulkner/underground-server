from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from undergroundapi.models import Artist
from django.db.models import Q
import uuid
from django.core.files.base import ContentFile
import base64


class ArtistView(ViewSet):
    """Rater events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        artists = Artist.objects.all()

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)



class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = Artist
        fields = ('id', 'name', 'social', 'image', 'description', 'spotify')
        depth = 1