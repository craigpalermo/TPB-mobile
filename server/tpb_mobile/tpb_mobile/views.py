from django.shortcuts import render
from django.views.generic.base import View
from django.template import RequestContext
from forms import SearchForm, TorrentForm, UserForm
from utils import match_category
from tpb import TPB
from tpb import ORDERS
from django.contrib.auth.models import User
from django.db import IntegrityError
from models import UserProfile
import settings
from django.http import HttpResponseRedirect
from utils import parse_torrent_page
from api.utils import create_torrent_record, delete_torrent_record

class SearchView(View):
    '''
    view for search page
    '''
    template_name = 'mobile/search.html'
    form_class = SearchForm
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if 'search_string' in request.GET:
            form = self.form_class(request.GET)
            torrent_form = TorrentForm()
        
            if form.is_valid():
                # get cleaned form data
                search_string = form.cleaned_data['search_string']
                category_string = form.cleaned_data['category']
                
                # construct search arguments
                # hardcoded to get first page, sort by number of seeders in descending order
                t = TPB(settings.TPB_URL)
                category = match_category(category_string)
                search = t.search(search_string, category=category).order(ORDERS.SEEDERS.ASC)
                results = search.page(1)
                        
            return render(request, self.template_name, {'form': form, 'results': results, 'torrent_form': torrent_form})
        else:          
            return render(request, self.template_name, {'form': form, 'results': None})

class QueueView(View):
    '''
    displays the list of torrents currently in the user's queue
    '''
    template_name = 'mobile/queue.html'
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next=/queue/')
        else:
            queue = UserProfile.objects.get(user=request.user).queue
            return render(request, self.template_name, {'queue': queue})           

class SettingsView(View):
    template_name = 'mobile/settings.html'
    
    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            client_id = profile.client_id if profile.client_id != None else "No client registered"
        except:    
            client_id = "Not logged in"
        return render(request, 'mobile/settings.html', {'client_id': client_id})
    
    def post(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            client_id = request.POST.get('client_id')
            profile.client_id = client_id
            profile.save()
        except:
            client_id = "Error retrieving client ID"
        return render(request, 'mobile/settings.html', {'client_id': client_id})

class RegistrationView(View):
    '''    
    form for new users to register
    '''
    form_class = UserForm
    template_name = 'mobile/registration/register.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        message = None
        
        if form.is_valid():
            cd = form.cleaned_data
            user = User()
            
            user.username = cd['username']    
            user.email = cd['email']
            user.set_password(cd['password'])
            
            try:
                user.save()
                
                # create UserProfile
                profile = UserProfile()
                profile.user = user
                profile.save()
                return HttpResponseRedirect('/')
            except IntegrityError:
                message = "The username you entered is taken"
            

        return render(request, self.template_name, {'form': form, 'message': message}, context_instance = RequestContext(request))
    
class TorrentPageView(View):
    '''
    displays the info page for a single torrent
    '''
    template_name ='mobile/torrent.html'
    
    def get(self, request, *args, **kwargs):
        url = kwargs.get('url')
        result = parse_torrent_page(url)
        dict2 = {'created': kwargs.get('created'), 'user': kwargs.get('user'),
                 'seeders': kwargs.get('seeders'), 'leechers': kwargs.get('leechers')}
        result.update(dict2)
        print result
        return render(request, self.template_name, {'data': result, 'url': url}, context_instance = RequestContext(request))
    
    def post(self, request, *args, **kwargs):
        form = TorrentForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            print cd
            data = {'seeders': cd.get('seeders'), 'title': cd.get('title'), 'url': cd.get('url'),
                    'torrent_link': cd.get('torrent_link'), 'magnet_link': cd.get('magnet_link'),
                    'size': cd.get('size'), 'leechers': cd.get('leechers'), 'created': cd.get('created'),
                    'user': cd.get('user')}
            result = parse_torrent_page(cd.get('url'))
            data.update(result)
            
        return render(request, self.template_name, {'data': data}, context_instance = RequestContext(request))
        
def torrent_form_middleman(request):
    '''
    directs the user to the correct view based on which link/button they clicked on the search or queue page
    '''
    if request.POST.get('link_action') == 'create_torrent':
        return create_torrent_record(request)
    elif request.POST.get('link_action') == 'delete_torrent':
        return delete_torrent_record(request)
    else:
        tpv = TorrentPageView()
        return tpv.post(request)
    