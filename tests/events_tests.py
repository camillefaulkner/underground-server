from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from undergroundapi.models import Event
from django.contrib.auth.models import User
from undergroundapi.views.event_view import EventSerializer
from datetime import date, datetime, timedelta

class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'categories', 'venues', 'events']
    
    def setUp(self):
        # Grab the first user object from the database and add their token to the headers
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_event(self):
        """Get event Test
        """
        # Grab a event object from the database
        event = Event.objects.first()

        url = f'/events/{event.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the event through the serializer that's being used in view
        expected = EventSerializer(event)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)

    def test_list_events(self):
        """Test list events"""
        url = '/events'

        response = self.client.get(url)
        
        # Get all the events in the database and serialize them to get the expected output
        all_events = Event.objects.filter(date__gte=date.today())
        expected = EventSerializer(all_events, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)


    def test_delete_event(self):
        """Test delete event"""
        event = Event.objects.first()

        url = f'/events/{event.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the event
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)