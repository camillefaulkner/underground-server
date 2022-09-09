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

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        user = request.auth.user
        artist = Artist.objects.get(pk=pk)
        if user.is_staff != True:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        
        if "image" in request.data and request.data["image"] is not None:
            if request.data["image"].startswith('/media'):
                pass 
            else:   
                format, imgstr = request.data["image"].split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')
                artist.image = data

        artist.name = request.data["name"]
        artist.social = request.data["social"] if "social" in request.data else None
        artist.spotify = request.data["spotify"] if "spotify" in request.data else None
        artist.description = request.data["description"]
        
        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT) 



class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = Artist
        fields = ('id', 'name', 'social', 'image', 'description', 'spotify')
        depth = 1