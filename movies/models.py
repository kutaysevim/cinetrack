from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    """Film/dizi türü (Aksiyon, Komedi, vb.)"""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Film veya dizi modeli"""
    TYPE_CHOICES = [
        ('movie', 'Film'),
        ('series', 'Dizi'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie')
    genres = models.ManyToManyField(Genre, blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    imdb_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True, null=True
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        """Kullanıcı yorumlarının ortalama puanını hesaplar"""
        reviews = self.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return None


class Review(models.Model):
    """Kullanıcı yorumu ve puanı"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')  # Bir kullanıcı bir filme bir yorum yapabilir

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Watchlist(models.Model):
    """Kullanıcının izleme listesi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"