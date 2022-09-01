from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from undergroundapi.models import Category
from django.db.models import Q
from django.contrib.auth.models import User


class UserView(ViewSet):
    """Rater events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 
        

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """

        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_staff')
        depth = 1