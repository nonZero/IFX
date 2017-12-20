from django.shortcuts import render, redirect

from movies.models import Movie, Movie_Tag_Field
from movies.forms import MovieForm



def home(request):
    qs = Movie.objects.order_by('?')[:10]
    d = {
        'objects': qs,
    }
    return render(request, "movies/home.html", d)


def detail(request, id):
    m = Movie.objects.get(id=id)
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
