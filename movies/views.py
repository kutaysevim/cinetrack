from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Movie, Genre, Review, Watchlist
from .forms import MovieForm, ReviewForm


def home(request):
    """Ana sayfa - öne çıkan filmler ve diziler"""
    from series.models import TVSeries
    featured_movies = Movie.objects.order_by('-created_at')[:3]
    featured_series = TVSeries.objects.order_by('-created_at')[:3]
    genres = Genre.objects.all()
    return render(request, 'movies/home.html', {
        'featured_movies': featured_movies,
        'featured_series': featured_series,
        'genres': genres,
    })


def movie_list(request):
    """Tüm filmlerin listesi - filtre ve sayfalama"""
    movies = Movie.objects.all().order_by('-created_at')

    genre_id = request.GET.get('genre')
    if genre_id:
        movies = movies.filter(genres__id=genre_id)

    paginator = Paginator(movies, 9)
    page = request.GET.get('page')
    movies = paginator.get_page(page)

    genres = Genre.objects.all()
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
    })


def movie_detail(request, pk):
    """Film detay sayfası"""
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.reviews.all().order_by('-created_at')
    review_form = ReviewForm()
    in_watchlist = False

    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(
            user=request.user, movie=movie
        ).exists()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'review_form': review_form,
        'in_watchlist': in_watchlist,
    })


@login_required
def movie_add(request):
    """Yeni film ekleme - sadece admin"""
    if not request.user.is_staff:
        messages.error(request, 'Bu işlem için yetkiniz yok!')
        return redirect('movies:movie_list')

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.created_by = request.user
            movie.save()
            form.save_m2m()
            messages.success(request, 'Film başarıyla eklendi!')
            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'Film Ekle'})


@login_required
def movie_edit(request, pk):
    """Film düzenleme - sadece admin"""
    if not request.user.is_staff:
        messages.error(request, 'Bu işlem için yetkiniz yok!')
        return redirect('movies:movie_list')

    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Film güncellendi!')
            return redirect('movies:movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'Film Düzenle'})


@login_required
def movie_delete(request, pk):
    """Film silme - sadece admin"""
    if not request.user.is_staff:
        messages.error(request, 'Bu işlem için yetkiniz yok!')
        return redirect('movies:movie_list')

    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Film silindi!')
        return redirect('movies:movie_list')
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})


@login_required
def add_review(request, pk):
    """Film yorumu ekleme"""
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, 'Yorumunuz eklendi!')
        else:
            messages.error(request, 'Bu filme zaten yorum yaptınız!')
    return redirect('movies:movie_detail', pk=pk)


@login_required
def toggle_watchlist(request, pk):
    """İzleme listesine ekle/çıkar"""
    movie = get_object_or_404(Movie, pk=pk)
    watchlist_item, created = Watchlist.objects.get_or_create(
        user=request.user, movie=movie
    )
    if not created:
        watchlist_item.delete()
        messages.info(request, 'İzleme listesinden çıkarıldı.')
    else:
        messages.success(request, 'İzleme listesine eklendi!')
    return redirect('movies:movie_detail', pk=pk)


@login_required
def watchlist(request):
    """Kullanıcının izleme listesi - film ve diziler"""
    from series.models import SeriesWatchlist
    movie_items = Watchlist.objects.filter(user=request.user).order_by('-added_at')
    series_items = SeriesWatchlist.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'movies/watchlist.html', {
        'movie_items': movie_items,
        'series_items': series_items,
    })


def search(request):
    """Film ve dizi arama"""
    from series.models import TVSeries
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Movie.objects.none()
    series = TVSeries.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else TVSeries.objects.none()

    return render(request, 'movies/search.html', {
        'movies': movies,
        'series': series,
        'query': query,
    })


def register(request):
    """Kullanıcı kayıt"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Hesabınız oluşturuldu!')
            return redirect('movies:home')
    else:
        form = UserCreationForm()
    return render(request, 'movies/register.html', {'form': form})