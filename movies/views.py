from builtins import super

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q

from movies.models import Movie, Collection, Tag, Field, Movie_Tag_Field, Movie_Title, Description
from movies.forms import MovieForm, CollectionForm, SearchByYearForm


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


def query(request, query):
    movies = []
    
    titles = Movie_Title.objects.filter(title__contains=query)
    if titles:
        for item in titles:
            movies.append(item.movie)
    description = Description.objects.filter(summery__icontains=query)
    if description:
        for item in description:
            movies.append(item.movie)
    tags = Tag.objects.filter(title__icontains=query)
    
    d = {
        'objects': movies,
        'count': len(movies)
    }
    return render(request, "movies/movies_list.html", d)


def movies_list(request):
    qs = Movie.objects.order_by('?')[:10]
    d = {
        'objects': qs,
        'count': len(Movie.objects.all())
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


def search_by_year(request):
    print('search_by_year')
    print('request={}'.format(request))
    search_query = request.POST.get('q', None)
    print('search_query={}'.format(search_query))
    id_select = request.POST.get('idselect', None)
    print('id_select={}'.format(id_select))
    if request.method == "POST":
        form = SearchByYearForm(request.POST)
        if form.is_valid():
            o = form.save(commit=False)
            qs = Movie.objects.filter(year=o.year)
            d = {
                'objects': qs,
                'count': len(qs),
                'query': 'year={}'.format(str(o.year)),
            }
            return render(request, "movies/search_result.html", d)
    else:
        form = SearchByYearForm()

    d = {
        'form': form,
    }
    return render(request, "movies/search_form.html", d)


class MoviesSearchListView(ListView):
    template_name = 'movies/searchresult.html'
    model = Movie
    context_object_name = 'movies'

    def get_queryset(self):
        qs = super(MoviesSearchListView, self).get_queryset()
        search_type = self.request.GET.get('type')
        q = self.request.GET.get('q')

        if q:
            if search_type == 'name':
                return qs.filter(title__icontain=q)
            elif search_type == 'year':
                if q.find('-') != -1:
                    q_list = q.split('-')
                    if q_list.isdigit():
                        year1 = q[0]
                        year2 = q[1]
                        if year1<year2:
                            return qs.filter(year__gte=int(year2)).exclude(year__gt=year1)
                        elif year1>year2:
                            return qs.filter(year__gte=int(year1)).exclude(year__gt=year2)
                else:
                    if q.isdigit():
                        return qs.filter(year__gte=int(q))

            elif search_type == 'director':
                pass
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def search_query(request):
    # Remove me
    print('search_query')
    print('request={}'.format(request))
    search_query = request.POST.get('q', None)
    print('search_query={}'.format(search_query))
    id_select = request.POST.get('idselect', None)
    print('id_select={}'.format(id_select))

    if request.method == "POST":
        q = request.POST.get('q', None)
        selection = request.POST.get('idselect', None)
        if q:
            if selection == 'all':  # Select All
                pass
            elif selection == 'title':  # Title
                return search_title(request, q)
            elif selection == 'year':  # Year/s
                return search_year(request, q)
            elif selection == 'director':  # Director
                return search_director(request, q)


def search_year(request, q):
    if q.find('-') != -1:
        q_list = q.split('-')
        year1 = q_list[0]
        year2 = q_list[1]
        if year1.isdigit() and year2.isdigit():
            if year1 >= year2:
                results = Movie.objects.filter(year__gte=int(year2)).exclude(year__gt=year1)
                query_str = 'Years={}-{}'.format(year2, year1)
                return search_results(request, results, query_str)
            elif year1 < year2:
                results = Movie.objects.filter(year__gte=int(year1)).exclude(year__gt=year2)
                query_str = 'Years={}-{}'.format(year1, year2)
                return search_results(request, results, query_str)
    elif q.isdigit():
        results = Movie.objects.filter(year=int(q))
        query_str = 'Year={}'.format(q)
        return search_results(request, results, query_str)

    # If we are here, error occurred
    error = '"{}" - Error in format'.format(q)
    print(error)
    return search_results(request, [], error)


def search_results(request, results, query_str):
    d = {
        'objects': results,
        'count': len(results),
        'query': query_str,
    }
    return render(request, "movies/search_result.html", d)


def search_title(request, query):
    qs = Movie_Title.objects.filter(title__icontains=query)
    results = []
    for item in qs:
        results.append(item.movie)

    query_str = 'Title="{}"'.format(query)
    return search_results(request, results, query_str)


def search_director(request, query):
    fields = Field.objects.filter(Q(title__icontains='במאי') | Q(title__icontains='director'))
    tags = Tag.objects.filter(title__icontains=query)
    qs = Movie_Tag_Field.objects.filter(Q(field__in=fields) & Q(tag__in=tags))
    results = []
    for item in qs:
        results.append(item.movie)

    query_str = 'Director="{}"'.format(query)
    return search_results(request, results, query_str)