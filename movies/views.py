from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from movies.models import Movie, Collection
from movies.forms import MovieForm, CollectionForm, CommentForm

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

    if request.method == "POST":
        import time
        time.sleep(3)
        form = CommentForm(request.POST)
        form.instance.movie = m
        if form.is_valid():
            c = form.save()
            return render(request, "movies/_comment.html", {
                'c': c,
            })
        return HttpResponseForbidden(
            form.errors.as_json(),
            content_type='application/json')
    d = {
        'movie': m,
        'form': CommentForm(),
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

def create_comment(request, id):
    o = get_object_or_404(Movie, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        form.instance.movie = o
        if form.is_valid():
            c = form.save()
            return redirect(o)
    else:
        # method = GET
        form = CommentForm()

    d = {
        'form': form,
    }
    return render(request, "movies/comment_form.html", d)