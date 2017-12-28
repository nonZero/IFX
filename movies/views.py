from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from movies.models import Movie, Collection
from movies.forms import MovieForm, CollectionForm

def homePage(request):
     return render(request, "movies/homePage.html")

def searchresult(request):
    return render(request, "movies/searchresult.html")

def movies_json(request):
    qs = Movie.objects.all()
    data = {
        'movies': [
            {
                'id': o.id,
                'title': o.title,
                'year': o.year,
                'lang': o.lang,
                'bid': o.bid,
            }
            for o in qs]
    }

    return JsonResponse(data)

def movies_list(request):
    qs = Movie.objects.order_by('?')[:10]
    d = {
        'objects': qs,
    }
    return render(request, "movies/movies_list.html", d)

def movie_detail(request, id):
    m = get_object_or_404(Movie, id=id)
    d = {
        'movie': m,
    }
    return render(request, "movies/movie_detail.html", d)

def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            o = form.save()
            return redirect("movies:movie_detail", id=o.id)
    else:
        # method = GET
        form = MovieForm()

    d = {
        'form': form,
    }
    return render(request, "movies/movie_form.html", d)

def collections_list(request):
    qs = Collection.objects.all()
    d = {
        'objects': qs,
    }
    return render(request, "movies/collections_list.html", d)

def collection_detail(request, id):
    c = get_object_or_404(Collection, id=id)
    d = {
        'collection': c,
    }
    return render(request, "movies/collection_detail.html", d)

def collection_create(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            o = form.save()
            return redirect("movies:collection_detail", id=o.id)
    else:
        # method = GET
        form = CollectionForm()

    d = {
        'form': form,
    }
    return render(request, "movies/collection_form.html", d)
