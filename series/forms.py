from django import forms
from .models import TVSeries, SeriesReview


class TVSeriesForm(forms.ModelForm):
    """Dizi ekleme/düzenleme formu"""
    class Meta:
        model = TVSeries
        fields = ['title', 'description', 'release_year', 'seasons', 'genres', 'poster', 'imdb_rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dizi adını girin'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Dizi hakkında kısa bir açıklama...'
            }),
            'release_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024'
            }),
            'seasons': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sezon sayısı'
            }),
            'genres': forms.CheckboxSelectMultiple(),
            'poster': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'imdb_rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.0 - 10.0',
                'step': '0.1'
            }),
        }


class SeriesReviewForm(forms.ModelForm):
    """Dizi yorum formu"""
    class Meta:
        model = SeriesReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': '1-10 arası puan'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Yorumunuzu yazın...'
            }),
        }