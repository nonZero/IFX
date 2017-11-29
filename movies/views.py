from django.shortcuts import render

from movies.models import Movie


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
