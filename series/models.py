from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.models import Genre


class TVSeries(models.Model):
    """Dizi modeli"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    genres = models.ManyToManyField(Genre, blank=True)
    poster = models.ImageField(upload_to='series_posters/', blank=True, null=True)
    imdb_rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True, null=True
    )
    seasons = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.series_reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return None

    class Meta:
        verbose_name = 'TV Series'
        verbose_name_plural = 'TV Series'


class SeriesReview(models.Model):
    """Dizi yorumu"""
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE, related_name='series_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('series', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.series.title}"


class SeriesWatchlist(models.Model):
    """Dizi izleme listesi"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(TVSeries, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'series')

    def __str__(self):
        return f"{self.user.username} - {self.series.title}"