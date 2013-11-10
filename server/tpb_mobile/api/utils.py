from tpb_mobile.forms import TorrentForm
from django.http import HttpResponse, HttpResponseRedirect
from tpb_mobile.models import Torrent, UserProfile
from django.contrib.auth import authenticate
import json
import tpb_mobile.settings as s

def create_torrent_record(request):
    '''
    adds a new torrent record to the database using form data from request
    '''
    if request.user.is_authenticated():
        form = TorrentForm(request.POST)
        new_torrent = form.save(commit=False)
        new_torrent.status = s.WAITING
        new_torrent.user = request.user
        new_torrent.save()
        return HttpResponseRedirect('/')
    else:
        message = "You must be logged in to add torrents to your queue"
        

def delete_torrent_record(request, torrent_id):
    try:
        Torrent.objects.get(id=torrent_id).delete()
        return HttpResponseRedirect('/queue/')
    except:
        pass

def register_client(request):
    '''
    attempts to authenticate using username and password. if successful, returns the user's uuid.
    if not, returns -1 to indicate error.
    '''
    username = request.POST('username', '')
    password = request.POST('password', '')
    
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            profile = UserProfile.objects.get(user=user)
            to_return = profile.uuid
        except:
            pass
    else:
        to_return = "-1"
    return HttpResponse(to_return, content_type="application/json")
        
        
def retrieve_queue(request, uuid, client_id):
    '''
    runs a query to get all torrent records linked to user that matches user_id,
    then serializes the resulting queryset as json and returns it
    '''
    try:
        profile = UserProfile.objects.get(uuid=uuid)
        
        if profile.client_id == client_id:
            records = Torrent.objects.filter(user=profile.user)
            
            for i in records:
                i.status = s.DOWNLOADED
                i.save()
                
            response_data = records.values()
            response = json.dumps([dict(id=record) for record in response_data])
        else:
            response = "-1"
    except:
        response = "-1"
        
    return HttpResponse(response, content_type="application/json")