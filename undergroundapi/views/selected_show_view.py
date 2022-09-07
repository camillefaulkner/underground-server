from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from undergroundapi.models import ChosenShow, Event
from datetime import date, datetime, timedelta

class SelectionView(ViewSet):
    """Rater events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            chosen = ChosenShow.objects.get(pk=pk)
            serializer = ChosenShowSerializer(chosen)
            return Response(serializer.data)
        except ChosenShow.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        chosenShows = ChosenShow.objects.filter(event__date__gte=date.today())
        user = request.query_params.get('user', None)
        if user is not None:
            chosenShows = chosenShows.filter(user_id=user)
        serializer = ChosenShowSerializer(chosenShows, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        event = Event.objects.get(pk=request.data["event"])

        chosen = ChosenShow.objects.create(
            event = event,
            user = request.auth.user
        )
        serializer = ChosenShowSerializer(chosen)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        chosen = ChosenShow.objects.get(pk=pk)
        user = request.auth.user
        if user.id != chosen.user.id:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)
        chosen.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ChosenShowSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = ChosenShow
        fields = ('id', 'event', 'user')
        depth = 1