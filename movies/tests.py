from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Movie, Genre, Review


class MovieModelTest(TestCase):
    """Film modeli testleri"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.genre = Genre.objects.create(name='Aksiyon')
        self.movie = Movie.objects.create(
            title='Test Film',
            description='Test açıklama',
            release_year=2024,
            type='movie',
            imdb_rating=8.5,
            created_by=self.user
        )
        self.movie.genres.add(self.genre)

    def test_movie_created(self):
        """Film oluşturuldu mu?"""
        self.assertEqual(self.movie.title, 'Test Film')
        self.assertEqual(self.movie.release_year, 2024)

    def test_movie_str(self):
        """Film __str__ metodu çalışıyor mu?"""
        self.assertEqual(str(self.movie), 'Test Film')

    def test_average_rating_no_reviews(self):
        """Yorum yokken ortalama puan None olmalı"""
        self.assertIsNone(self.movie.average_rating())

    def test_average_rating_with_reviews(self):
        """Yorumlarla ortalama puan hesaplanıyor mu?"""
        Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=8,
            comment='Güzel film'
        )
        self.assertEqual(self.movie.average_rating(), 8.0)


class MovieViewTest(TestCase):
    """Film view testleri"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Film',
            description='Test açıklama',
            release_year=2024,
            type='movie',
            created_by=self.user
        )

    def test_home_page(self):
        """Ana sayfa açılıyor mu?"""
        response = self.client.get(reverse('movies:home'))
        self.assertEqual(response.status_code, 200)

    def test_movie_list_page(self):
        """Film listesi açılıyor mu?"""
        response = self.client.get(reverse('movies:movie_list'))
        self.assertEqual(response.status_code, 200)

    def test_movie_detail_page(self):
        """Film detay sayfası açılıyor mu?"""
        response = self.client.get(
            reverse('movies:movie_detail', kwargs={'pk': self.movie.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_movie_add_requires_login(self):
        """Film ekleme giriş gerektiriyor mu?"""
        response = self.client.get(reverse('movies:movie_add'))
        self.assertEqual(response.status_code, 302)

    def test_search(self):
        """Arama çalışıyor mu?"""
        response = self.client.get(reverse('movies:search') + '?q=Test')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        """Kayıt sayfası açılıyor mu?"""
        response = self.client.get(reverse('movies:register'))
        self.assertEqual(response.status_code, 200)