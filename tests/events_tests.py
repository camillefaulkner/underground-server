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

    # def test_create_event(self):
    #     """Create event test"""
    #     url = "/events"

    #     # Define the Game properties
    #     # The keys should match what the create method is expecting
    #     # Make sure this matches the code you have
    #     game = {
    #         "title": "Clue",
    #         "maker": "Milton Bradley",
    #         "skill_level": 5,
    #         "number_of_players": 6,
    #         "game_type": 1,
    #     }

    #     response = self.client.post(url, game, format='json')

    #     # The _expected_ output should come first when using an assertion with 2 arguments
    #     # The _actual_ output will be the second argument
    #     # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
    #     # Get the last game added to the database, it should be the one just created
    #     new_game = Game.objects.last()

    #     # Since the create method should return the serialized version of the newly created game,
    #     # Use the serializer you're using in the create method to serialize the "new_game"
    #     # Depending on your code this might be different
    #     expected = GameSerializer(new_game)

    #     # Now we can test that the expected ouput matches what was actually returned
    #     self.assertEqual(expected.data, response.data)

    # def test_change_game(self):
    #     """test update game"""
    #     # Grab the first game in the database
    #     game = Game.objects.first()

    #     url = f'/games/{game.id}'

    #     updated_game = {
    #         "title": f'{game.title} updated',
    #         "maker": game.maker,
    #         "skill_level": game.skill_level,
    #         "number_of_players": game.number_of_players,
    #         "game_type": game.game_type.id
    #     }

    #     response = self.client.put(url, updated_game, format='json')

    #     self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    #     # Refresh the game object to reflect any changes in the database
    #     game.refresh_from_db()

    #     # assert that the updated value matches
    #     self.assertEqual(updated_game['title'], game.title)

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