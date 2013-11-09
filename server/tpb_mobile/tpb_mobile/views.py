from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from forms import SearchForm, TorrentForm
from utils import match_category
from tpb import TPB
from tpb import CATEGORIES, ORDERS
import settings



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
        torrent_form = TorrentForm()
        
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
            
            return render(request, self.template_name, {'form': form, 'results': results, 'torrent_form': torrent_form})
        else:
            form = self.form_class()
        
        return render(request, 'search.html', {'form': form, 'torrent_form': torrent_form})
    
def create_torrent_record(request):
    '''
    adds a new torrent record to the database using form data from request
    '''
    form = TorrentForm(request.POST)
    new_torrent = form.save()
    new_torrent.save()
    return HttpResponse("Torrent record successfully createds")
    