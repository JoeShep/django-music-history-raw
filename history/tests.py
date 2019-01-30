import unittest
from django.test import TestCase
from django.urls import reverse
from .models import Artist

# Stuff to test
# context: what we send to the template
# content: the rendered html
# response_codes

# Name your tests like this! test_foo so Django can find and run 'em

# * The test client is a Python class that acts as a dummy Web browser, allowing you to test your views and interact with your Django - powered application programmatically. Some of the things you can do with the test client are:
#     * Simulate GET and POST requests on a URL and observe the response – everything from low - level HTTP(result headers and status codes) to page content.
#     * See the chain of redirects(if any) and check the URL and status code at each step.
#     * Test that a given request is rendered by a given Django template, with a template context that contains certain values.

# *  Good rules-of-thumb include having:
#     * a separate TestClass for each model or view
#     * a separate test method for each set of conditions you want to test
#     * test method names that describe their function

class ArtistTest(TestCase):

    def test_list_artists(self):
        new_artist = Artist.objects.create(
            name="Suzy Saxophone",
            birth_date="12/25/58",
            biggest_hit="Honk Honk Squeak"
        )

        # Issue a GET request. "client" is a dummy web browser
        # 'reverse' is used to generate a URL for a given view. The main advantage is that you do not hard code routes in your code.
        response = self.client.get(reverse('history:artists'))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 1 artist.
        # Response.context is the context variable passed to the template by the view. This is incredibly useful for testing, because it allows us to confirm that our template is getting all the data it needs.
        self.assertEqual(len(response.context['artist_list']), 1)

        # .encode converts from unicode to utf-8
        # example:
        # If the string is: pythön!
        # The encoded version is: b'pyth\xc3\xb6n!'
        self.assertIn(new_artist.name.encode(), response.content)

    def test_get_artist_form(self):

      response = self.client.get(reverse('history:artist_form'))

      self.assertIn(
          '<input type="text" name="name" maxlength="100" required id="id_name">'.encode(), response.content)

    def test_post_artist(self):

      response = self.client.post(reverse('history:artist_form'), {'name': 'Bill Board', 'birth_date': '10/31/67', 'biggest_hit': "So Blue Fer You"})

      # Getting 302 back because we have a success url and the view is redirecting
      self.assertEqual(response.status_code, 302)

    def test_get_artist_detail(self):
      new_artist = Artist.objects.create(
          name="Suzy Saxophone",
          birth_date="12/25/58",
          biggest_hit="Honk Honk Squeak"
      )

      response = self.client.get(reverse('history:artist_detail', args=(1,)))
      self.assertEqual(response.context["artist_detail"].name, new_artist.name)
