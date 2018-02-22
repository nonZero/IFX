from django.views.generic import ListView

from enrich.models import Suggestion
from ifx.base_views import IFXMixin


class SuggestionListView(IFXMixin, ListView):
    model = Suggestion
    paginate_by = 100
