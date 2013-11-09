from tpb_mobile.forms import TorrentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from tpb_mobile.models import Torrent
import json
import tpb_mobile.settings as s

def create_torrent_record(request):
    '''
    adds a new torrent record to the database using form data from request
    '''
    form = TorrentForm(request.POST)
    new_torrent = form.save(commit=False)
    new_torrent.status = s.WAITING
    new_torrent.user = request.user
    new_torrent.save()
    return HttpResponseRedirect('/')

def delete_torrent_record(request, torrent_id):
    try:
        Torrent.objects.get(id=torrent_id).delete()
        return HttpResponseRedirect('/queue/')
    except:
        pass

def retrieve_queue(request, user_id):
    '''
    runs a query to get all torrent records linked to user that matches user_id,
    then serializes the resulting queryset as json and returns it
    '''
    user = User.objects.get(id=user_id)
    records = Torrent.objects.filter(user=user)
    
    for i in records:
        i.status = s.DOWNLOADED
        i.save()
        
    response_data = records.values()
    response = json.dumps([dict(id=record) for record in response_data])
    return HttpResponse(response, content_type="application/json")