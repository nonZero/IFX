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
        'tags': o.tags.names(),
    }
    return render(request, "movies/detail.html", d)

def create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            # without tagging:
            # o = form.save()
            # for using tagging:
            o = form.save(commit=False)
            o.user = request.user
            o.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            return redirect("movies:detail", id=o.id)
    else:
        # method = GET
        form = MovieForm()

    d = {
        'form': form,
    }
    return render(request, "movies/form.html", d)
