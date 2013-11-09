from django import forms
from django.forms import ModelForm
from models import Torrent

class SearchForm(forms.Form):
    CATEGORY_CHOICES = ( ('ALL', 'All'),
                         ('APPLICATIONS', 'Applications'),
                         ('AUDIO', 'Audio'),
                         ('GAMES', 'Games'),
                         ('VIDEO', 'Video'),
                         ('OTHER', 'Other') )
    search_string = forms.CharField(max_length=50)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    
class TorrentForm(ModelForm):
    class Meta:
        model = Torrent
        fields = ['title', 'url', 'magnet_link', 'torrent_link', 'size', 'seeders']
            
class UserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value = True))