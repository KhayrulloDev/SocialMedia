from myapp.models import Movie  # Assuming Movie model is defined in myapp
from django.test import TestCase, Client
from django.urls import reverse


class TestMovieSortingViewTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title='Avengers', director='Joss Whedon', year=2012, imdb_rating=8.0)
        Movie.objects.create(title='Avatar', director='James Cameron', year=2009, imdb_rating=7.8)
        Movie.objects.create(title='Inception', director='Christopher Nolan', year=2010, imdb_rating=8.8)

    def test_movie_sorting_view(self):
        client = Client()

        url = reverse('/movie-sort-list/')

        response = client.get(url, {'ordering': '-imdb_rating'})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0]['title'], 'Inception')
        self.assertEqual(response.data[1]['title'], 'Avengers')
        self.assertEqual(response.data[2]['title'], 'Avatar')

