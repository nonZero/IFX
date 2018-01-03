from builtins import super

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from movies.models import Movie, Collection
from movies.forms import MovieForm, CollectionForm

def homePage(request):
     return render(request, "movies/homePage.html", {'set_jumbotron':1})

def about(request):
    return render(request, "movies/about.html", {'set_jumbotron':2})

def searchresult(request):
    return render(request, "movies/searchresult.html", {'set_jumbotron':3})

def movie_details(request):
    return render(request, "movies/movie_details.html", {'set_jumbotron':3})


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


#class MoviesSearchListView(ListView):
#    template_name = 'movies/searchresult.html'
#    set_jumbotron = 3
#    model = Movie
#    context_object_name = 'movies'

#    def get_queryset(self):
#        qs = super(MoviesSearchListView, self).get_queryset()
#        search_type = self.request.GET.get('type')
#        q = self.request.GET.get('q')
#        if q:
#            if search_type == 'name':
#                return qs.filter(title__icontain=q)
#            elif search_type == 'year':
#                q_list = q.split('-')
#                year1 = q[0]
#                year2 = q[1]
#                return qs.filter(year__gte=int(year1)).exclude(year__gt=year2)
#            elif search_type == 'director':
#                pass
#        return []

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context