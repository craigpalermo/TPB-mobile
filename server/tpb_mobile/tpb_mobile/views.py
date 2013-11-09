from django.shortcuts import render
from django.views.generic.base import View
from forms import SearchForm, TorrentForm
from utils import match_category
from tpb import TPB
from tpb import CATEGORIES, ORDERS
from models import Torrent
import settings
from django.http import HttpResponseRedirect

class SearchView(View):
    '''
    view for search page
    '''
    template_name = 'search.html'
    form_class = SearchForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        username = request.user.username if request.user.is_authenticated() else None
          
        return render(request, self.template_name, {'form': form, 'results': None,
                                                    'logged_in': request.user.is_authenticated(),
                                                    'username': username})
    
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

class QueueView(View):
    '''
    displays the list of torrents currently in the user's queue
    '''
    template_name = 'queue.html'
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        else:
            queue = Torrent.objects.filter(user=request.user, status=settings.WAITING)
            username = request.user.username if request.user.is_authenticated() else None
            return render(request, self.template_name, {'queue': queue, 
                                                        'logged_in': request.user.is_authenticated(),
                                                        'username': username})           
