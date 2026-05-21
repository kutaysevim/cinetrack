from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

app_name = 'movies'

router = DefaultRouter()
router.register(r'movies', api_views.MovieViewSet)
router.register(r'genres', api_views.GenreViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movies/add/', views.movie_add, name='movie_add'),
    path('movies/<int:pk>/edit/', views.movie_edit, name='movie_edit'),
    path('movies/<int:pk>/delete/', views.movie_delete, name='movie_delete'),
    path('movies/<int:pk>/review/', views.add_review, name='add_review'),
    path('movies/<int:pk>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('search/', views.search, name='search'),
    path('accounts/register/', views.register, name='register'),
    path('api/', include(router.urls)),
]