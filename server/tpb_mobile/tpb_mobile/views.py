from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import View

from tpb import TPB
from tpb import CATEGORIES, ORDERS
import settings
from forms import SearchForm
from utils import match_category

class SearchView(View):
    '''
    view for search page
    '''
    template_name = 'search.html'
    form_class = SearchForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'results': None})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # get cleaned form data
            search_string = form.cleaned_data['search_string']
            category_string = form.cleaned_data['category']
            
            # construct search arguments
            # hardcoded to get first page, sort by num. of seeders in descending order
            t = TPB(settings.TPB_URL)
            category = match_category(category_string)
            search = t.search(search_string, category=category).order(ORDERS.SEEDERS.ASC)
            results = search.page(1)
            
            return render(request, self.template_name, {'form': form, 'results': results})
        else:
            form = self.form_class()
        
        return render(request, 'search.html', {'form': form})
    