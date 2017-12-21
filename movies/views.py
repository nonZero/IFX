from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from movies.models import Movie, Collection
from movies.forms import MovieForm

def home_json(request):
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

def home(request):
    qs = Movie.objects.order_by('?')[:10]
    d = {
        'objects': qs,
    }
    return render(request, "movies/home.html", d)


def detail(request, id):
    m = get_object_or_404(Movie, id=id)
    d = {
        'movie': m,
    }
    return render(request, "movies/detail.html", d)

def create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            o = form.save()
            return redirect("movies:detail", id=o.id)
    else:
        # method = GET
        form = MovieForm()

    d = {
        'form': form,
    }
    return render(request, "movies/form.html", d)

def collections_list(request):
    qs = Collection.objects.all()
    d = {
        'objects': qs,
    }
    return render(request, "movies/collections_list.html", d)
