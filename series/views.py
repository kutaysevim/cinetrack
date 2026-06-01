from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import TVSeries, SeriesReview, SeriesWatchlist
from .forms import TVSeriesForm, SeriesReviewForm


def series_list(request):
    """Tüm dizilerin listesi"""
    series = TVSeries.objects.all().order_by('-created_at')

    genre_id = request.GET.get('genre')
    if genre_id:
        series = series.filter(genres__id=genre_id)

    paginator = Paginator(series, 9)
    page = request.GET.get('page')
    series = paginator.get_page(page)

    from movies.models import Genre
    genres = Genre.objects.all()
    return render(request, 'series/series_list.html', {
        'series': series,
        'genres': genres,
    })


def series_detail(request, pk):
    """Dizi detay sayfası"""
    series = get_object_or_404(TVSeries, pk=pk)
    reviews = series.series_reviews.all().order_by('-created_at')
    review_form = SeriesReviewForm()
    in_watchlist = False

    if request.user.is_authenticated:
        in_watchlist = SeriesWatchlist.objects.filter(
            user=request.user, series=series
        ).exists()

    return render(request, 'series/series_detail.html', {
        'series': series,
        'reviews': reviews,
        'review_form': review_form,
        'in_watchlist': in_watchlist,
    })


@login_required
def series_add(request):
    """Yeni dizi ekleme - sadece admin"""
    if not request.user.is_staff:
        messages.error(request, 'Bu işlem için yetkiniz yok!')
        return redirect('series:series_list')

    if request.method == 'POST':
        form = TVSeriesForm(request.POST, request.FILES)
        if form.is_valid():
            series = form.save(commit=False)
            series.created_by = request.user
            series.save()
            form.save_m2m()
            messages.success(request, 'Dizi başarıyla eklendi!')
            return redirect('series:series_detail', pk=series.pk)
    else:
        form = TVSeriesForm()
    return render(request, 'series/series_form.html', {'form': form, 'title': 'Dizi Ekle'})


@login_required
def series_edit(request, pk):
    """Dizi düzenleme - sadece admin"""
    if not request.user.is_staff:
        messages.error(request, 'Bu işlem için yetkiniz yok!')
        return redirect('series:series_list')

    series = get_object_or_404(TVSeries, pk=pk)
    if request.method == 'POST':
        form = TVSeriesForm(request.POST, request.FILES, instance=series)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dizi güncellendi!')
            return redirect('series:series_detail', pk=series.pk)
    else:
        form = TVSeriesForm(instance=series)
    return render(request, 'series/series_form.html', {'form': form, 'title': 'Dizi Düzenle'})


@login_required
def series_delete(request, pk):
    """Dizi silme - sadece admin"""
    if not request.user.is_staff:
        messages.error(request, 'Bu işlem için yetkiniz yok!')
        return redirect('series:series_list')

    series = get_object_or_404(TVSeries, pk=pk)
    if request.method == 'POST':
        series.delete()
        messages.success(request, 'Dizi silindi!')
        return redirect('series:series_list')
    return render(request, 'series/series_confirm_delete.html', {'series': series})


@login_required
def add_review(request, pk):
    """Dizi yorumu ekleme"""
    series = get_object_or_404(TVSeries, pk=pk)
    if request.method == 'POST':
        form = SeriesReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.series = series
            review.user = request.user
            review.save()
            messages.success(request, 'Yorumunuz eklendi!')
        else:
            messages.error(request, 'Bu diziye zaten yorum yaptınız!')
    return redirect('series:series_detail', pk=pk)


@login_required
def toggle_watchlist(request, pk):
    """İzleme listesine ekle/çıkar"""
    series = get_object_or_404(TVSeries, pk=pk)
    watchlist_item, created = SeriesWatchlist.objects.get_or_create(
        user=request.user, series=series
    )
    if not created:
        watchlist_item.delete()
        messages.info(request, 'İzleme listesinden çıkarıldı.')
    else:
        messages.success(request, 'İzleme listesine eklendi!')
    return redirect('series:series_detail', pk=pk)