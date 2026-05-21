from django import forms
from .models import Movie, Review


class MovieForm(forms.ModelForm):
    """Film ekleme/düzenleme formu"""
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_year', 'type', 'genres', 'poster', 'imdb_rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Film adını girin'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Film hakkında kısa bir açıklama...'
            }),
            'release_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
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


class ReviewForm(forms.ModelForm):
    """Yorum formu"""
    class Meta:
        model = Review
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