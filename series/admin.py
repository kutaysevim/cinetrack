from django.contrib import admin
from .models import TVSeries, SeriesReview, SeriesWatchlist
from movies.models import Genre


@admin.register(TVSeries)
class TVSeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_year', 'imdb_rating', 'seasons', 'created_by']
    list_filter = ['genres', 'release_year']
    search_fields = ['title', 'description']


@admin.register(SeriesReview)
class SeriesReviewAdmin(admin.ModelAdmin):
    list_display = ['series', 'user', 'rating', 'created_at']


@admin.register(SeriesWatchlist)
class SeriesWatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'series', 'added_at']