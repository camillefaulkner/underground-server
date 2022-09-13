from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from undergroundapi.models import Venue, Category
from rest_framework.decorators import action
from django.db.models import Q


class VenueView(ViewSet):
    """Rater events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            venue = Venue.objects.get(pk=pk)
            serializer = VenueSerializer(venue)
            return Response(serializer.data)
        except Venue.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        venues = Venue.objects.all()

        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)


    @action(methods=["put"], detail=True) #detail True adds pk to the URL
    def assign_category(self, request, pk):
        venue = Venue.objects.get(pk=pk)
        category = Category.objects.get(pk = request.data["category"])
        venue.category = category
        venue.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)



class VenueSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = Venue
        fields = ('id', 'name', 'address', ' private', 'category', 'user')
        depth = 1