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
    """Ana sayfa - öne çıkan filmler"""
    featured_movies = Movie.objects.order_by('-created_at')[:6]
    genres = Genre.objects.all()
    return render(request, 'movies/home.html', {
        'featured_movies': featured_movies,
        'genres': genres,
    })


def movie_list(request):
    """Tüm film/dizilerin listesi - filtre ve sayfalama"""
    movies = Movie.objects.all().order_by('-created_at')

    # Tür filtresi
    genre_id = request.GET.get('genre')
    if genre_id:
        movies = movies.filter(genres__id=genre_id)

    # Film/dizi filtresi
    type_filter = request.GET.get('type')
    if type_filter in ['movie', 'series']:
        movies = movies.filter(type=type_filter)

    # Sayfalama (sayfa başına 9 film)
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
    """Yeni film/dizi ekleme"""
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
    """Film/dizi düzenleme"""
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
    """Film/dizi silme"""
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
    """Kullanıcının izleme listesi"""
    items = Watchlist.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'movies/watchlist.html', {'items': items})


def search(request):
    """Film/dizi arama"""
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Movie.objects.none()

    return render(request, 'movies/search.html', {
        'movies': movies,
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