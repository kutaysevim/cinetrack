from rest_framework import serializers
from .models import Movie, Genre, Review


class GenreSerializer(serializers.ModelSerializer):
    """Tür serializer"""
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    """Yorum serializer"""
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']


class MovieSerializer(serializers.ModelSerializer):
    """Film serializer"""
    genres = GenreSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_year',
            'type', 'genres', 'imdb_rating', 'average_rating',
            'reviews', 'created_at'
        ]

    def get_average_rating(self, obj):
        return obj.average_rating()
