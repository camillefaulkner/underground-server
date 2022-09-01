from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from undergroundapi.models import Event, Venue, Artist
from django.db.models import Q
import uuid
from django.core.files.base import ContentFile
import base64

from undergroundapi.models.category_model import Category


class EventView(ViewSet):
    """Rater events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            evt = Event.objects.get(pk=pk)
            serializer = EventSerializer(evt)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        events = Event.objects.all()
        approved = request.query_params.get('approved', None)
        if approved is not None:
            events = events.filter(approved=approved)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        user = request.auth.user

        if "image" in request.data["evt"]:
            format, imgstr = request.data["evt"]["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["evt"]["name"]}-{uuid.uuid4()}.{ext}')

        category = Category.objects.get(pk=request.data["venue"]["category"])

        if "id" not in request.data["venue"]:
            venue = Venue.objects.create(
                name=request.data["venue"]["name"],
                address=request.data["venue"]["address"],
                private=request.data["venue"]["private"],
                category=category,
                user=user
            )
        else:
            venue = Venue.objects.get(pk=request.data["venue"]["id"])

        evt = Event.objects.create(
            name=request.data["evt"]["name"],
            image=data if "image" in request.data["evt"] else None,
            date=request.data["evt"]["date"],
            time=request.data["evt"]["time"],
            description=request.data["evt"]["description"],
            user=user,
            venue=venue
        )

        for artist in request.data["artists"]:
            artist = Artist.objects.create(
                name=artist["name"],
                social= artist["social"] if "social" in artist else None,
                # image=data,
                description=artist["description"],
                spotify=artist["spotify"] if "spotify" in artist else None
            )
            evt.artists.add(artist.id)
        serializer = EventSerializer(evt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        user = request.auth.user
        event = Event.objects.get(pk=pk)
        if user.is_staff != True:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        
        if request.data["image"].startswith('/media'):
            pass
        else:
            format, imgstr = request.data["image"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["name"]}-{uuid.uuid4()}.{ext}')
            event.image = data

        # event.approved = request.data["approved"]
        event.name = request.data["name"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.description = request.data["description"]
        
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        user = request.auth.user
        if user.is_staff == False:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = Event
        fields = ('id', 'name', 'image', 'date', 'time', 'description', 'approved','user', 'venue', 'artists')
        depth = 1