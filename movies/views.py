from django.shortcuts import render, redirect

from movies.models import Movie
from movies.forms import MovieForm



def home(request):
    qs = Movie.objects.order_by('-date')
    d = {
        'objects': qs,
    }
    return render(request, "movies/home.html", d)


def detail(request, id):
    o = Movie.objects.get(id=id)
    d = {
        'object': o,
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
