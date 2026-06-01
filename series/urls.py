from django.urls import path
from . import views

app_name = 'series'

urlpatterns = [
    path('', views.series_list, name='series_list'),
    path('<int:pk>/', views.series_detail, name='series_detail'),
    path('add/', views.series_add, name='series_add'),
    path('<int:pk>/edit/', views.series_edit, name='series_edit'),
    path('<int:pk>/delete/', views.series_delete, name='series_delete'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
    path('<int:pk>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
]