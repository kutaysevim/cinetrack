from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """Film API - Listeleme, detay, ekleme, güncelleme, silme"""
    queryset = Movie.objects.all().order_by('-created_at')
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['release_year', 'imdb_rating', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    """Tür API"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]