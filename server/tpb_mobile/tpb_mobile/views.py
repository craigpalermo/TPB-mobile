from django.shortcuts import render
from django.views.generic.base import View
from django.template import RequestContext
from forms import SearchForm, TorrentForm, UserForm
from utils import match_category
from tpb import TPB
from tpb import CATEGORIES, ORDERS
from django.contrib.auth.models import User
from models import Torrent, UserProfile
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

class QueueView(View):
    '''
    displays the list of torrents currently in the user's queue
    '''
    template_name = 'queue.html'
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next=/queue/')
        else:
            queue = Torrent.objects.filter(user=request.user, status=settings.WAITING)
            return render(request, self.template_name, {'queue': queue})           

class SettingsView(View):
    template_name = 'settings.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, 'settings.html')
    

class RegistrationView(View):
    '''    
    form for new users to register
    '''
    form_class = UserForm
    template_name = 'registration/register.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User()
            
            user.username = cd['username']    
            user.email = cd['email']
            user.password = cd['password']
            user.save()
            
            # create UserProfile
            profile = UserProfile()
            profile.user = user
            profile.save()
                
            return HttpResponseRedirect('/')

        return render(request, self.template_name, {'form': form}, context_instance = RequestContext(request))
    